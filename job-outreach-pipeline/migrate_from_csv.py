import os
import sys
import csv
import shutil
import argparse
from datetime import datetime
from collections import Counter

import db
import applicant


class DryRunRollback(Exception):
    """Internal sentinel exception used to rollback dry-run transactions."""
    pass


def is_person_name(name):
    """Checks if recipient_name looks like a person rather than a generic team."""
    if not name:
        return False
    words = name.strip().split()
    if not words:
        return False
    if any(w.lower().strip(",.&") in applicant.GENERIC_RECIPIENT_WORDS for w in words):
        return False
    return True


def classify_email(email, company_domain=None):
    """person / departmental / generic, using the same rules as enrichment (db.classify_address)."""
    return db.classify_address(email, company_domain)


def is_usable_email(email):
    """True if email is non-empty, not 'no_email_found', and contains '@'."""
    if not email:
        return False
    clean = email.strip().lower()
    return clean != "" and clean != "no_email_found" and "@" in clean


def backup_database(db_path):
    """Copies existing DB file to outreach.db.bak-YYYYmmdd-HHMMSS."""
    if db_path != ":memory:" and os.path.exists(db_path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak_path = f"{db_path}.bak-{ts}"
        shutil.copy2(db_path, bak_path)
        print(f"[Migrate] Backed up existing database to {bak_path}")
        return bak_path
    return None


def migrate(queue_path=None, log_path=None, db_path=None, dry_run=False):
    """
    Runs migration from queue and log CSVs into SQLite database in ONE transaction.
    If dry_run=True, rolls back transaction at the end.
    Returns dict with stats and verification results.
    """
    if db_path is None:
        db_path = db.DB_PATH
    if queue_path is None:
        queue_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach_queue.csv")
    if log_path is None:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach_log.csv")

    if not dry_run:
        backup_database(db_path)

    queue_rows = []
    if os.path.exists(queue_path):
        with open(queue_path, "r", encoding="utf-8", newline="") as f:
            queue_rows = list(csv.DictReader(f))

    log_rows = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8", newline="") as f:
            log_rows = list(csv.DictReader(f))

    conn = db.connect(db_path)

    companies_inserted = 0
    contacts_inserted = 0
    outreaches_inserted = 0
    synthesized_initial_count = 0
    report_lines = []
    verified = False

    try:
        with db.transaction(conn):
            # 1. Queue rows -> companies
            for r in queue_rows:
                name = r["company_name"].strip()
                website = r.get("website", "").strip()
                company_type = r.get("company_type", "").strip()
                company_address = r.get("company_address", "").strip()
                scope = r.get("scope", "").strip()
                ghana_eligibility = r.get("ghana_eligibility", "").strip()
                evidence_url = r.get("evidence_url", "").strip()
                careers_url = r.get("careers_url", "").strip()
                status = r.get("status", "Pending").strip()
                date_added = r.get("date_added", "").strip()
                created_at = (f"{date_added} 00:00:00" if len(date_added) == 10 else date_added) if date_added else None

                _, created = db.upsert_company(
                    conn, name,
                    website=website,
                    company_type=company_type,
                    company_address=company_address,
                    scope=scope,
                    ghana_eligibility=ghana_eligibility,
                    evidence_url=evidence_url,
                    careers_url=careers_url,
                    status=status,
                    created_at=created_at,
                    # Lets 'enrich --status Skipped' revive companies the old scraper gave up on
                    notes="no_contact_found" if status == "Skipped" and not is_usable_email(r.get("email")) else None,
                )
                if created:
                    companies_inserted += 1

            # 2. Queue rows -> contacts
            for r in queue_rows:
                raw_email = r.get("email", "").strip()
                if not is_usable_email(raw_email):
                    continue
                name = r["company_name"].strip()
                comp = db.get_company_by_name(conn, name)
                if not comp:
                    continue
                company_id = comp["id"]
                clean_email = raw_email.lower().strip()
                email_kind = classify_email(clean_email, comp["domain"] or comp["website"])
                recip_name = r.get("recipient_name", "").strip()
                full_name = recip_name if is_person_name(recip_name) else None

                existing_c = conn.execute(
                    "SELECT id FROM contacts WHERE lower(email) = lower(?)",
                    (clean_email,)
                ).fetchone()

                db.add_contact(
                    conn, company_id=company_id, email=clean_email,
                    full_name=full_name, source="apify", email_kind=email_kind,
                    make_primary=(email_kind != "generic")  # a generic inbox is never the primary
                )
                if not existing_c:
                    contacts_inserted += 1

            # 3. Log rows -> outreaches
            for r in log_rows:
                comp_name = r["company_name"].strip()
                email = r["email"].strip().lower()
                log_status = r["status"].strip()
                sent_at = r["date"].strip()
                cover_letter = r.get("cover_letter", "").strip() or None

                comp = db.get_company_by_name(conn, comp_name)
                if not comp:
                    continue
                company_id = comp["id"]

                cont = db.find_contact_by_email(conn, email)
                contact_id = cont["id"] if cont else None

                role = applicant.role_for(comp["company_type"]) if comp["company_type"] else applicant.DEFAULT_ROLE
                subj = applicant.subject(role)

                existing_o = conn.execute(
                    """SELECT id FROM outreaches
                    WHERE company_id = ? AND recipient_email = ? AND email_type = 'initial' AND sent_at = ?""",
                    (company_id, email, sent_at)
                ).fetchone()

                if not existing_o:
                    conn.execute(
                        """INSERT INTO outreaches (
                            company_id, contact_id, recipient_email, email_type, subject,
                            message_id, status, sent_at, cover_letter_path
                        ) VALUES (?, ?, ?, 'initial', ?, NULL, ?, ?, ?)""",
                        (company_id, contact_id, email, subj, log_status, sent_at, cover_letter)
                    )
                    outreaches_inserted += 1

            # 4. Queue date_sent -> initial and followup outreaches
            for r in queue_rows:
                date_sent_raw = r.get("date_sent", "").strip()
                comp_name = r["company_name"].strip()
                q_status = r.get("status", "").strip()
                raw_email = r.get("email", "").strip()
                email = raw_email.lower().strip() if is_usable_email(raw_email) else ""

                if not date_sent_raw and q_status not in ("Sent", "Followup-Sent"):
                    continue

                comp = db.get_company_by_name(conn, comp_name)
                if not comp:
                    continue
                company_id = comp["id"]

                cont = db.find_contact_by_email(conn, email) if email else None
                contact_id = cont["id"] if cont else None

                role = applicant.role_for(comp["company_type"]) if comp["company_type"] else applicant.DEFAULT_ROLE
                subj = applicant.subject(role)

                initial_date = None
                followup_date = None
                if "| Followup:" in date_sent_raw:
                    parts = date_sent_raw.split("| Followup:", 1)
                    initial_date = parts[0].strip()
                    followup_date = parts[1].strip()
                elif date_sent_raw:
                    initial_date = date_sent_raw

                # Initial outreach synthesis if Sent/Followup-Sent and no initial outreach exists yet
                if initial_date and (q_status in ("Sent", "Followup-Sent") or initial_date):
                    existing_init = conn.execute(
                        "SELECT id FROM outreaches WHERE company_id = ? AND email_type = 'initial'",
                        (company_id,)
                    ).fetchone()
                    if not existing_init:
                        letter = applicant.letter_filename(comp_name)
                        conn.execute(
                            """INSERT INTO outreaches (
                                company_id, contact_id, recipient_email, email_type, subject,
                                message_id, status, sent_at, cover_letter_path
                            ) VALUES (?, ?, ?, 'initial', ?, NULL, 'SUCCESS', ?, ?)""",
                            (company_id, contact_id, email, subj, initial_date, letter)
                        )
                        outreaches_inserted += 1
                        synthesized_initial_count += 1

                # Followup outreach synthesis if date_sent had followup date
                if followup_date:
                    existing_followup = conn.execute(
                        """SELECT id FROM outreaches
                        WHERE company_id = ? AND email_type = 'followup' AND sent_at = ?""",
                        (company_id, followup_date)
                    ).fetchone()
                    if not existing_followup:
                        followup_subj = f"Re: {subj}"
                        conn.execute(
                            """INSERT INTO outreaches (
                                company_id, contact_id, recipient_email, email_type, subject,
                                message_id, status, sent_at, cover_letter_path
                            ) VALUES (?, ?, ?, 'followup', ?, NULL, 'SUCCESS', ?, NULL)""",
                            (company_id, contact_id, email, followup_subj, followup_date)
                        )
                        outreaches_inserted += 1

            # 5. Verification checks
            csv_queue_count = len(queue_rows)
            db_companies_count = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
            check_companies = (csv_queue_count == db_companies_count)

            csv_status_counts = Counter(r.get("status", "").strip() for r in queue_rows)
            db_status_rows = conn.execute("SELECT status, COUNT(*) AS cnt FROM companies GROUP BY status").fetchall()
            db_status_counts = {row["status"]: row["cnt"] for row in db_status_rows}
            check_statuses = all(db_status_counts.get(s, 0) == count for s, count in csv_status_counts.items())

            csv_log_success_count = sum(1 for r in log_rows if r.get("status", "").strip() == "SUCCESS")
            expected_initial_success = csv_log_success_count + synthesized_initial_count
            db_initial_success_count = conn.execute(
                "SELECT COUNT(*) FROM outreaches WHERE email_type = 'initial' AND status = 'SUCCESS'"
            ).fetchone()[0]
            check_outreaches = (expected_initial_success == db_initial_success_count)

            csv_usable_emails_count = sum(1 for r in queue_rows if is_usable_email(r.get("email")))
            db_contacts_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
            check_contacts = (csv_usable_emails_count == db_contacts_count)

            verified = check_companies and check_statuses and check_outreaches and check_contacts

            # Build report lines
            report_lines.append("[Migrate] ==================== Migration Report ====================")
            report_lines.append(f"[Migrate] Database: {db_path}")
            report_lines.append(f"[Migrate] Mode:     {'DRY-RUN' if dry_run else 'LIVE'}")
            report_lines.append(f"[Migrate] Inserts performed:")
            report_lines.append(f"[Migrate]   Companies:  {companies_inserted}")
            report_lines.append(f"[Migrate]   Contacts:   {contacts_inserted}")
            report_lines.append(f"[Migrate]   Outreaches: {outreaches_inserted}")
            report_lines.append("[Migrate] -------------------- Verification --------------------")
            report_lines.append(
                f"[Migrate] 1. Companies count:      CSV={csv_queue_count:<4} DB={db_companies_count:<4} "
                f"[{'OK' if check_companies else 'FAIL'}]"
            )
            status_details = ", ".join(f"{s}={count} (DB={db_status_counts.get(s, 0)})" for s, count in sorted(csv_status_counts.items()))
            report_lines.append(
                f"[Migrate] 2. Status buckets:       {status_details} "
                f"[{'OK' if check_statuses else 'FAIL'}]"
            )
            report_lines.append(
                f"[Migrate] 3. Initial SUCCESS:      Expected={expected_initial_success:<4} DB={db_initial_success_count:<4} "
                f"[{'OK' if check_outreaches else 'FAIL'}]"
            )
            report_lines.append(
                f"[Migrate] 4. Usable emails:        Queue={csv_usable_emails_count:<4} DB={db_contacts_count:<4} "
                f"[{'OK' if check_contacts else 'FAIL'}]"
            )
            report_lines.append("[Migrate] ==========================================================")
            report_lines.append(f"[Migrate] Verification result: {'SUCCESS' if verified else 'MISMATCH'}")

            for line in report_lines:
                print(line)

            if dry_run:
                raise DryRunRollback()

    except DryRunRollback:
        pass

    return {
        "companies_inserted": companies_inserted,
        "contacts_inserted": contacts_inserted,
        "outreaches_inserted": outreaches_inserted,
        "verified": verified,
        "report": "\n".join(report_lines),
    }


def main():
    parser = argparse.ArgumentParser(description="Migrate CSV outreach queue and log into SQLite database.")
    parser.add_argument("--queue", default=None, help="Path to outreach_queue.csv")
    parser.add_argument("--log", default=None, help="Path to outreach_log.csv")
    parser.add_argument("--db", default=None, help="Path to SQLite database file")
    parser.add_argument("--dry-run", action="store_true", help="Run migration in a transaction then rollback")
    args = parser.parse_args()

    result = migrate(
        queue_path=args.queue,
        log_path=args.log,
        db_path=args.db,
        dry_run=args.dry_run
    )

    if not result["verified"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
