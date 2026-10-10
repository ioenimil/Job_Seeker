import os
import sys
import time
import random
import applicant
from email_sender import EmailSender
import check_inbox
import db


def run_followups(conn=None, limit=10, dry_run=True, check_inbox_first=True):
    """
    Runs the follow-up pipeline on top of SQLite.
    Fetches candidates via db.followup_candidates(conn, min_days=6).
    In live mode:
      - Runs check_inbox.run_check first (aborts live run if IMAP check fails)
      - Sends follow-up email with threading headers and CV attachment
      - Records send in SQLite with db.record_send (one transaction per send)
      - Waits 30-60s between sends
    In dry-run mode:
      - Prints recipient, subject, and threading header status
    Returns summary dict: {"sent": int, "candidates": int, "aborted": bool}
    """
    close_conn = False
    if conn is None:
        conn = db.connect()
        close_conn = True

    try:
        # 1. Check inbox first if requested
        if check_inbox_first:
            try:
                print("[Followup] Checking inbox for recent replies/bounces...")
                check_inbox.run_check(conn=conn, dry_run=dry_run)
            except Exception as e:
                if dry_run:
                    print(f"[Followup] Warning: Inbox check failed during dry-run: {e}. Continuing dry-run.")
                else:
                    print(f"[Followup] ERROR: Inbox check failed during live run: {e}. Aborting follow-up run.")
                    return {"aborted": True, "sent": 0, "error": str(e), "candidates": 0}

        # 2. Query candidates from SQLite
        candidates = db.followup_candidates(conn, min_days=6)
        print(f"[Followup] Found {len(candidates)} candidate(s) due for follow-up.")
        if not candidates:
            return {"sent": 0, "candidates": 0, "aborted": False}

        to_send = candidates[:limit]
        print(f"[Followup] Processing batch of {len(to_send)} follow-up(s) (dry_run={dry_run})...")

        sender = None
        if not dry_run:
            sender = EmailSender()

        # Locate CV
        cv_path = applicant.CV_PATH
        if not os.path.exists(cv_path):
            alt_cv = os.path.join(os.path.dirname(os.path.abspath(__file__)), applicant.CV_PATH)
            if os.path.exists(alt_cv):
                cv_path = alt_cv

        sent_count = 0
        for idx, c in enumerate(to_send):
            comp_name = c["company_name"]
            recipient_email = c["recipient_email"]
            role_title = c["role_title"] or applicant.role_for(c["company_type"])
            initial_subject = c["initial_subject"] or applicant.subject(role_title)
            subject = initial_subject if initial_subject.startswith("Re: ") else f"Re: {initial_subject}"
            in_reply_to = c["initial_message_id"]
            references = c["initial_message_id"]

            has_threading = bool(in_reply_to)
            threading_desc = f"YES (In-Reply-To: {in_reply_to})" if has_threading else "NO (legacy NULL id)"

            if dry_run:
                print(f"[DRY-RUN] Recipient: {recipient_email} ({comp_name}) | Subject: {subject} | Threading headers: {threading_desc}")
            else:
                recipient_name = c["full_name"] or ""
                sender_email = sender.sender_email

                body_text = (
                    f"{applicant.salutation(recipient_name)},\n\n"
                    f"I hope this email finds you well.\n\n"
                    f"I am writing to follow up briefly on my application for {role_title} opportunities at {comp_name} sent last week.\n\n"
                    f"I remain very interested in the work your team is doing, and wanted to check if there are any updates or if you would be open to a brief 10-minute call to connect. "
                    f"I would be glad to share how my experience with platform engineering on AWS and Kubernetes, GitOps delivery, observability, and shipping applied AI systems for clients can support your team's goals.\n\n"
                    f"I have attached my updated CV for your convenience. Please let me know if there is any other information I can provide.\n\n"
                    f"Thank you for your time and consideration.\n\n"
                    f"Best regards,\n\n"
                    + applicant.signature()
                )

                original_date = c["initial_sent_at"]
                body_text += (
                    f"\n\n---\n"
                    f"Original Message:\n"
                    f"From: {sender_email}\n"
                    f"Sent: {original_date}\n"
                    f"Subject: {initial_subject}\n\n"
                    + applicant.outreach_body(comp_name, role_title)
                )

                attachments = (cv_path,) if os.path.exists(cv_path) else ()

                print(f"[Followup] Sending follow-up to {recipient_email} ({threading_desc})...")
                res = sender.send_followup(
                    recipient_email=recipient_email,
                    subject=subject,
                    body=body_text,
                    in_reply_to=in_reply_to,
                    references=references,
                    attachments=attachments
                )

                # Record send in DB — one transaction per send
                db.record_send(
                    conn=conn,
                    company_id=c["company_id"],
                    contact_id=c["contact_id"],
                    recipient_email=recipient_email,
                    email_type="followup",
                    subject=subject,
                    message_id=res.get("message_id"),
                    in_reply_to=in_reply_to,
                    references=references,
                    status="SUCCESS" if res["ok"] else "FAILED",
                    error=res.get("error"),
                    new_company_status="Followup-Sent" if res["ok"] else None
                )

                if res["ok"]:
                    sent_count += 1

                # Delay between sends to avoid rate limits / spam flags
                if idx < len(to_send) - 1:
                    delay = random.randint(30, 60)
                    print(f"[Followup] Waiting {delay}s before next send...")
                    time.sleep(delay)

        print(f"[Followup] Batch complete. Sent: {sent_count} / {len(to_send)}.")
        return {"sent": sent_count, "candidates": len(candidates), "aborted": False}
    finally:
        if close_conn:
            conn.close()


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    is_live = len(args) > 0 and args[0] == "run"
    run_followups(limit=10, dry_run=not is_live)


if __name__ == "__main__":
    main()
