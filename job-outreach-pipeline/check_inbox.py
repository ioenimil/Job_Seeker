import imaplib
import email
import email.utils
import email.header
import re
import os
import sys
import argparse
from datetime import datetime, timedelta
from config import config
import db


def get_decoded_header(msg, header_name):
    """Safely decode an email header into a unicode string."""
    val = msg.get(header_name, "")
    if not val:
        return ""
    try:
        parts = email.header.decode_header(val)
        decoded = []
        for text, enc in parts:
            if isinstance(text, bytes):
                decoded.append(text.decode(enc or "utf-8", errors="replace"))
            else:
                decoded.append(str(text))
        return "".join(decoded)
    except Exception:
        return str(val)


def extract_body_and_snippet(msg):
    """Extract full plain text body and a clean 250-character snippet."""
    text_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    text_parts.append(payload.decode("utf-8", errors="replace"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text_parts.append(payload.decode("utf-8", errors="replace"))

    full_body = "\n".join(text_parts).strip()
    collapsed = " ".join(full_body.split())
    snippet = collapsed[:250] if collapsed else ""
    return full_body, snippet


def extract_unquoted_text(body):
    """
    Extracts only new text from email body, excluding:
    - lines starting with '>'
    - any lines after a quote intro like 'On ... wrote:', '--- Original Message ---', or 'From: ... Sent: ...'
    """
    lines = body.splitlines()
    unquoted_lines = []

    for line in lines:
        stripped = line.strip()
        if re.search(r'on\s+.+wrote\s*:', stripped, re.IGNORECASE):
            break
        if re.search(r'---+.*original message', stripped, re.IGNORECASE):
            break
        if re.search(r'^from:\s+.+sent:', stripped, re.IGNORECASE):
            break
        if stripped.startswith(">"):
            continue
        unquoted_lines.append(line)

    return "\n".join(unquoted_lines).strip()


def parse_message_date(msg):
    """Parse Date header to YYYY-MM-DD HH:MM:SS format."""
    date_str = msg.get("Date")
    if date_str:
        try:
            dt = email.utils.parsedate_to_datetime(date_str)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    return db.now_iso()


def send_desktop_notification(title, message):
    """Attempt desktop notification via notify-send, ignoring any failures."""
    try:
        import shutil
        import subprocess
        if shutil.which("notify-send"):
            subprocess.run(["notify-send", title, message], check=False, timeout=3)
    except Exception:
        pass


def resolve_associations(conn, from_email, msg):
    """Resolve company_id, contact_id, outreach_id, and company_name from DB."""
    company_id = None
    contact_id = None
    outreach_id = None
    company_name = None

    if not conn:
        return company_id, contact_id, outreach_id, company_name

    # 1. Match by contact email
    if from_email:
        contact = db.find_contact_by_email(conn, from_email)
        if contact:
            contact_id = contact["id"]
            company_id = contact["company_id"]
            company_name = contact["company_name"]

    # 2. Match by company domain
    if not company_id and from_email and "@" in from_email:
        sender_domain = db.bare_domain(from_email.split("@")[1])
        comp = db.find_company_by_domain(conn, sender_domain)
        if comp:
            company_id = comp["id"]
            company_name = comp["name"]

    # 3. Match by In-Reply-To or References
    in_reply_to = msg.get("In-Reply-To", "")
    references = msg.get("References", "")
    headers_combined = f"{in_reply_to} {references}"
    mids = re.findall(r'<[^>]+>', headers_combined)
    if not mids and (in_reply_to.strip() or references.strip()):
        mids = [in_reply_to.strip()] if in_reply_to.strip() else [references.strip()]

    for mid in mids:
        mid_clean = mid.strip()
        row = conn.execute("SELECT * FROM outreaches WHERE message_id = ?", (mid_clean,)).fetchone()
        if row:
            if not outreach_id:
                outreach_id = row["id"]
            if not company_id:
                company_id = row["company_id"]
                comp = db.get_company(conn, company_id)
                if comp:
                    company_name = comp["name"]
            if not contact_id:
                contact_id = row["contact_id"]
            break

    return company_id, contact_id, outreach_id, company_name


def classify_message(msg, conn=None):
    """
    Pure, unit-testable classifier for an email Message.
    Classifies into ('bounce', 'auto_reply', 'unsubscribe', 'reply', 'unrelated') in strict order.
    Returns (kind, details_dict).
    """
    from_raw = get_decoded_header(msg, "From")
    from_email = email.utils.parseaddr(from_raw)[1].lower().strip()
    subject = get_decoded_header(msg, "Subject").strip()
    full_body, snippet = extract_body_and_snippet(msg)
    received_at = parse_message_date(msg)

    imap_msg_id = msg.get("Message-ID", "").strip()
    if not imap_msg_id:
        import hashlib
        h = hashlib.sha256(f"{from_email}:{subject}:{received_at}".encode()).hexdigest()[:16]
        imap_msg_id = f"<{h}@inbox>"

    details = {
        "from_email": from_email,
        "subject": subject,
        "snippet": snippet,
        "received_at": received_at,
        "imap_message_id": imap_msg_id,
        "company_id": None,
        "contact_id": None,
        "outreach_id": None,
        "company_name": None,
        "failed_recipients": []
    }

    # 0. IGNORE OWN MAIL (SENDER_EMAIL): e.g. copies or self-sent tests
    sender_email_cfg = config.get("SENDER_EMAIL")
    if sender_email_cfg:
        sender_email_clean = email.utils.parseaddr(sender_email_cfg)[1].lower().strip()
        if from_email and from_email == sender_email_clean:
            return "unrelated", details

    # 1. BOUNCE:
    # - From mailer-daemon@ or postmaster@
    # - OR multipart/report with report-type=delivery-status
    # - OR X-Failed-Recipients header
    content_type_raw = str(msg.get("Content-Type", "")).lower()
    msg_type = msg.get_content_type().lower()
    is_dsn = (msg_type == "multipart/report" and "delivery-status" in content_type_raw)
    if not is_dsn and msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type().lower() == "message/delivery-status":
                is_dsn = True
                break

    is_mailer_daemon = from_email.startswith("mailer-daemon@") or from_email.startswith("postmaster@")
    has_failed_header = bool(msg.get("X-Failed-Recipients"))

    if is_mailer_daemon or is_dsn or has_failed_header:
        failed_recipients = []
        if has_failed_header:
            for item in msg.get("X-Failed-Recipients", "").split(","):
                parsed = email.utils.parseaddr(item)[1].lower().strip()
                if parsed and parsed not in failed_recipients:
                    failed_recipients.append(parsed)

        # Check Final-Recipient in headers and subparts
        for part in msg.walk():
            fr = part.get("Final-Recipient")
            if fr:
                fr_clean = fr.split(";", 1)[1].strip() if ";" in fr else fr.strip()
                fr_addr = email.utils.parseaddr(fr_clean)[1].lower().strip() or fr_clean.lower().strip()
                if fr_addr and "@" in fr_addr and fr_addr not in failed_recipients:
                    failed_recipients.append(fr_addr)

        # Check body for failed recipients
        body_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', full_body)
        for be in body_emails:
            be_clean = be.lower().strip()
            if conn:
                if db.find_contact_by_email(conn, be_clean) or conn.execute("SELECT 1 FROM outreaches WHERE lower(recipient_email) = lower(?)", (be_clean,)).fetchone():
                    if be_clean not in failed_recipients:
                        failed_recipients.append(be_clean)
            elif be_clean not in failed_recipients and be_clean != from_email:
                failed_recipients.append(be_clean)

        details["failed_recipients"] = failed_recipients

        # Resolve company / contact in DB
        if conn and failed_recipients:
            for fr_email in failed_recipients:
                contact = db.find_contact_by_email(conn, fr_email)
                if contact:
                    details["contact_id"] = contact["id"]
                    details["company_id"] = contact["company_id"]
                    details["company_name"] = contact["company_name"]
                    break
                o_row = conn.execute("SELECT * FROM outreaches WHERE lower(recipient_email) = lower(?) ORDER BY id DESC LIMIT 1", (fr_email,)).fetchone()
                if o_row:
                    details["outreach_id"] = o_row["id"]
                    details["company_id"] = o_row["company_id"]
                    details["contact_id"] = o_row["contact_id"]
                    comp = db.get_company(conn, o_row["company_id"])
                    if comp:
                        details["company_name"] = comp["name"]
                    break

        return "bounce", details

    # 1.5. BULK / MARKETING / LIST MAIL FILTER:
    # Treat bulk/list mail as 'unrelated' (List-Id, List-Unsubscribe, or Precedence: bulk/list/junk)
    # UNLESS In-Reply-To/References matches one of our stored outreach message_ids
    has_list_header = bool(msg.get("List-Id") or msg.get("List-Unsubscribe"))
    precedence_bulk = msg.get("Precedence", "").strip().lower() in ("bulk", "list", "junk")

    if has_list_header or precedence_bulk:
        matches_stored_outreach = False
        if conn:
            in_reply_to = msg.get("In-Reply-To", "")
            references = msg.get("References", "")
            headers_combined = f"{in_reply_to} {references}"
            mids = re.findall(r'<[^>]+>', headers_combined)
            if not mids and (in_reply_to.strip() or references.strip()):
                mids = [in_reply_to.strip()] if in_reply_to.strip() else [references.strip()]
            for mid in mids:
                if conn.execute("SELECT 1 FROM outreaches WHERE message_id = ?", (mid.strip(),)).fetchone():
                    matches_stored_outreach = True
                    break

        if not matches_stored_outreach:
            return "unrelated", details

    # 2. AUTO-REPLY:
    # - Auto-Submitted other than 'no'
    # - X-Autoreply / X-Autorespond
    # - Precedence: auto_reply
    # - Subject like "Automatic reply", "Out of office", "Auto:", "OOO:"
    auto_sub = msg.get("Auto-Submitted", "").strip().lower()
    is_auto_sub = bool(auto_sub and auto_sub != "no")
    has_autoreply_header = bool(msg.get("X-Autoreply") or msg.get("X-Autorespond"))
    precedence_auto = (msg.get("Precedence", "").strip().lower() == "auto_reply")
    subj_lower = subject.lower()
    subject_auto = (
        "automatic reply" in subj_lower
        or "out of office" in subj_lower
        or subj_lower.startswith("auto:")
        or "ooo:" in subj_lower
    )

    if is_auto_sub or has_autoreply_header or precedence_auto or subject_auto:
        comp_id, cont_id, out_id, comp_name = resolve_associations(conn, from_email, msg)
        details["company_id"] = comp_id
        details["contact_id"] = cont_id
        details["outreach_id"] = out_id
        details["company_name"] = comp_name
        return "auto_reply", details

    # 3. UNSUBSCRIBE:
    # Human message whose UNQUOTED text asks to be removed, AND associated with company/outreach
    unsub_phrases = ["unsubscribe", "remove me", "stop emailing", "not interested"]
    unquoted_body_lower = extract_unquoted_text(full_body).lower()
    if any(phrase in unquoted_body_lower for phrase in unsub_phrases):
        comp_id, cont_id, out_id, comp_name = resolve_associations(conn, from_email, msg)
        if comp_id is not None or out_id is not None:
            details["company_id"] = comp_id
            details["contact_id"] = cont_id
            details["outreach_id"] = out_id
            details["company_name"] = comp_name
            return "unsubscribe", details
        else:
            return "unrelated", details

    # 4. REPLY:
    # Sender matches contact email, OR company domain, OR In-Reply-To/References matches outreach message_id
    comp_id, cont_id, out_id, comp_name = resolve_associations(conn, from_email, msg)
    details["company_id"] = comp_id
    details["contact_id"] = cont_id
    details["outreach_id"] = out_id
    details["company_name"] = comp_name

    has_threading = bool(msg.get("In-Reply-To") or msg.get("References"))

    if comp_id is not None or out_id is not None:
        return "reply", details
    if conn is None and has_threading:
        return "reply", details

    # 5. UNRELATED:
    return "unrelated", details


def find_sent_folder(imap):
    """Find Sent Mail folder via LIST and the \\Sent special-use flag."""
    status, folder_list = imap.list()
    if status == 'OK' and folder_list:
        for item in folder_list:
            item_str = item.decode('utf-8', errors='replace') if isinstance(item, bytes) else str(item)
            if "\\Sent" in item_str:
                match = re.search(r'"([^"]+)"\s*$', item_str.strip())
                if match:
                    return match.group(1)
                parts = item_str.strip().split()
                return parts[-1]
    return "[Gmail]/Sent Mail"


def backfill_message_ids(conn, imap):
    """
    Backfills outreach Message-IDs for legacy SUCCESS rows with NULL message_id.
    Searches Gmail Sent folder via LIST and \\Sent special-use flag, readonly.
    Returns count of updated outreaches.
    """
    rows = conn.execute(
        "SELECT * FROM outreaches WHERE status = 'SUCCESS' AND (message_id IS NULL OR message_id = '')"
    ).fetchall()
    if not rows:
        print("[Backfill] No outreaches need Message-ID backfill.")
        return 0

    sent_folder = find_sent_folder(imap)
    print(f"[Backfill] Selecting Sent folder: {sent_folder} (readonly)")
    status, _ = imap.select(f'"{sent_folder}"', readonly=True)
    if status != "OK":
        status, _ = imap.select(sent_folder, readonly=True)
        if status != "OK":
            print(f"[Backfill] Could not open Sent folder {sent_folder}.")
            return 0

    backfilled_count = 0
    for r in rows:
        outreach_id = r["id"]
        recipient = r["recipient_email"]
        stored_subject = (r["subject"] or "").strip().lower()
        sent_at = r["sent_at"]

        try:
            sent_dt = datetime.strptime(sent_at.split()[0], "%Y-%m-%d")
            since_dt = sent_dt - timedelta(days=2)
            before_dt = sent_dt + timedelta(days=3)
            since_str = since_dt.strftime("%d-%b-%Y")
            before_str = before_dt.strftime("%d-%b-%Y")
            search_query = f'(HEADER TO "{recipient}" SINCE "{since_str}" BEFORE "{before_str}")'
        except Exception:
            search_query = f'(HEADER TO "{recipient}")'

        search_status, data = imap.search(None, search_query)
        if search_status != "OK" or not data or not data[0]:
            search_status, data = imap.search(None, f'(HEADER TO "{recipient}")')

        if search_status == "OK" and data and data[0]:
            msg_ids = data[0].split()
            for mid in msg_ids:
                fetch_status, fetch_data = imap.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID SUBJECT)])')
                if fetch_status == "OK" and fetch_data:
                    raw_header = None
                    for item in fetch_data:
                        if isinstance(item, tuple) and len(item) > 1:
                            raw_header = item[1]
                            break
                    if raw_header:
                        header_msg = email.message_from_bytes(raw_header)
                        hdr_subject = get_decoded_header(header_msg, "Subject").strip().lower()
                        if not stored_subject or (stored_subject == hdr_subject or stored_subject in hdr_subject or hdr_subject in stored_subject):
                            found_msg_id = header_msg.get("Message-ID", "").strip()
                            if found_msg_id:
                                db.set_outreach_message_id(conn, outreach_id, found_msg_id)
                                backfilled_count += 1
                                print(f"[Backfill] Outreach {outreach_id} ({recipient}) -> {found_msg_id}")
                                break

    try:
        imap.close()
    except Exception:
        pass

    print(f"[Backfill] Finished backfill. Updated {backfilled_count} / {len(rows)} outreaches.")
    return backfilled_count


def test_connection():
    """Login, select INBOX readonly, print message count, logout."""
    sender_email = config.get("SENDER_EMAIL")
    password = config.get("GMAIL_APP_PASSWORD")
    if not sender_email or not password:
        print("[CheckInbox] Error: SENDER_EMAIL or GMAIL_APP_PASSWORD missing in config.")
        return False
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(sender_email, password)
        status, data = imap.select("INBOX", readonly=True)
        count = data[0].decode() if data and data[0] else "0"
        print(f"[CheckInbox] Successfully connected to IMAP. INBOX message count: {count}")
        try:
            imap.close()
        except Exception:
            pass
        imap.logout()
        return True
    except Exception as e:
        print(f"[CheckInbox] IMAP connection test failed: {e}")
        return False


def run_check(conn=None, days=None, dry_run=False, backfill=True):
    """
    Checks Gmail inbox via IMAP (strictly read-only).
    Classifies messages, updates DB, alerts on replies.
    Returns dict summary.
    """
    close_conn = False
    if conn is None:
        conn = db.connect()
        close_conn = True

    sender_email = config.get("SENDER_EMAIL")
    password = config.get("GMAIL_APP_PASSWORD")
    if not sender_email or not password:
        if close_conn:
            conn.close()
        raise ValueError("SENDER_EMAIL or GMAIL_APP_PASSWORD missing in config.")

    counts = {
        "events": 0,
        "replies": 0,
        "bounces": 0,
        "auto_replies": 0,
        "unsubscribes": 0,
        "unrelated": 0,
        "backfilled": 0
    }

    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(sender_email, password)

        # Backfill legacy Message-IDs if requested
        if backfill and not dry_run:
            counts["backfilled"] = backfill_message_ids(conn, imap)

        # Strictly READ-ONLY INBOX select
        select_status, _ = imap.select("INBOX", readonly=True)
        if select_status != "OK":
            raise RuntimeError("Failed to select INBOX in readonly mode.")

        # Compute SINCE date
        if days is not None:
            since_dt = datetime.now() - timedelta(days=days)
        else:
            earliest = None
            row = conn.execute("SELECT MIN(sent_at) AS min_sent FROM outreaches WHERE status = 'SUCCESS'").fetchone()
            if row and row["min_sent"]:
                try:
                    earliest = datetime.strptime(row["min_sent"].split()[0], "%Y-%m-%d")
                except Exception:
                    pass
            since_dt = earliest if earliest is not None else (datetime.now() - timedelta(days=30))

        since_str = since_dt.strftime("%d-%b-%Y")
        print(f"[CheckInbox] Searching INBOX for messages SINCE {since_str} (strictly readonly)...")

        search_status, data = imap.search(None, f'(SINCE "{since_str}")')
        if search_status != "OK" or not data or not data[0]:
            print("[CheckInbox] No messages returned from search.")
            msg_nums = []
        else:
            msg_nums = data[0].split()

        for num in msg_nums:
            # Use BODY.PEEK to never mark messages as seen
            fetch_status, fetch_data = imap.fetch(num, '(BODY.PEEK[])')
            if fetch_status != "OK" or not fetch_data:
                continue

            raw_bytes = None
            for item in fetch_data:
                if isinstance(item, tuple) and len(item) > 1:
                    raw_bytes = item[1]
                    break
            if not raw_bytes:
                continue

            msg = email.message_from_bytes(raw_bytes)
            kind, details = classify_message(msg, conn=conn)

            if kind in ("unrelated", None):
                counts["unrelated"] += 1
                continue

            if dry_run:
                print(f"[DRY-RUN] Classified message from {details['from_email']} as '{kind}': {details['subject']}")
                if kind == "reply":
                    counts["replies"] += 1
                elif kind == "bounce":
                    counts["bounces"] += 1
                elif kind == "auto_reply":
                    counts["auto_replies"] += 1
                elif kind == "unsubscribe":
                    counts["unsubscribes"] += 1
                continue

            # Live run: record inbox event and update status atomically in one transaction
            with db.transaction(conn):
                event_id, created = db.record_inbox_event(
                    conn,
                    kind=kind,
                    from_email=details["from_email"],
                    imap_message_id=details["imap_message_id"],
                    subject=details["subject"],
                    received_at=details["received_at"],
                    snippet=details["snippet"],
                    company_id=details.get("company_id"),
                    contact_id=details.get("contact_id"),
                    outreach_id=details.get("outreach_id")
                )

                if not created:
                    # Already processed previously
                    continue

                counts["events"] += 1

                if kind == "bounce":
                    counts["bounces"] += 1
                    contact_id = details.get("contact_id")
                    if contact_id:
                        conn.execute(
                            "UPDATE contacts SET verification_status = 'invalid', updated_at = ? WHERE id = ?",
                            (db.now_iso(), contact_id)
                        )
                    company_id = details.get("company_id")
                    if company_id:
                        comp = db.get_company(conn, company_id)
                        if comp and comp["status"] not in ("Replied", "Bounced"):
                            db.set_company_status(conn, company_id, "Bounced")

                elif kind == "auto_reply":
                    counts["auto_replies"] += 1
                    # Record event only, no status change

                elif kind == "unsubscribe":
                    counts["unsubscribes"] += 1
                    company_id = details.get("company_id")
                    if company_id:
                        comp = db.get_company(conn, company_id)
                        if comp:
                            existing_notes = comp["notes"] or ""
                            if "unsubscribe" not in existing_notes.lower():
                                new_notes = f"{existing_notes}; unsubscribe".strip("; ")
                            else:
                                new_notes = existing_notes
                            db.update_company(conn, company_id, notes=new_notes)
                            if comp["status"] not in ("Replied", "Bounced"):
                                db.set_company_status(conn, company_id, "Replied")

                elif kind == "reply":
                    counts["replies"] += 1
                    company_id = details.get("company_id")
                    comp_name = details.get("company_name")
                    if company_id:
                        comp = db.get_company(conn, company_id)
                        if comp:
                            comp_name = comp_name or comp["name"]
                            if comp["status"] not in ("Replied", "Bounced"):
                                db.set_company_status(conn, company_id, "Replied")

            if kind == "reply":
                comp_name = details.get("company_name")
                print(f"\n{'='*60}")
                print(f"[REPLY ALERT] Company: {comp_name or 'Unknown'}")
                print(f"              Sender:  {details['from_email']}")
                print(f"              Subject: {details['subject']}")
                print(f"              Snippet: {details['snippet']}")
                print(f"{'='*60}\n")

                send_desktop_notification(
                    f"Outreach Reply: {comp_name or details['from_email']}",
                    f"{details['from_email']}: {details['subject']}"
                )

        try:
            imap.close()
        except Exception:
            pass
        try:
            imap.logout()
        except Exception:
            pass

        return counts
    finally:
        if close_conn:
            conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check Gmail inbox via IMAP for replies, bounces, etc.")
    parser.add_argument("--days", type=int, default=None, help="Check messages received in the last N days")
    parser.add_argument("--dry-run", action="store_true", help="Classify and print, write nothing to DB")
    parser.add_argument("--test-connection", action="store_true", help="Test IMAP login and INBOX access")
    parser.add_argument("--no-backfill", action="store_true", help="Skip backfilling legacy outreach Message-IDs")
    args = parser.parse_args(argv)

    if args.test_connection:
        success = test_connection()
        return 0 if success else 1

    summary = run_check(
        days=args.days,
        dry_run=args.dry_run,
        backfill=not args.no_backfill
    )
    print(f"[CheckInbox] Done. Summary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
