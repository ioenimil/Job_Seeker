import os
import sys
import time
import random
import argparse
import requests
from urllib.parse import urlparse
import db
import applicant

LETTERS_DIR = "generated_letters"
CV_PATH = applicant.CV_PATH
DAILY_SEND_LIMIT = 15
GENERIC_RECIPIENT = "The Recruiting and Technology Team"

COMPANY_TYPES = ["general_startup", "consultancy", "fintech", "isp", "bank", "ai"]

EMPLOYER_RULES = (
    "Return only real companies that employ software, platform, DevOps, cloud or AI engineers. "
    "Drop listicles, job boards, news sites, directories, government regulators, recruiters and staffing agencies; "
    "return the employer itself, never the page that lists it. "
    "website must be the company's own homepage. company_type: fintech for payments/lending/financial software, "
    "bank for banks, isp for telecoms and internet providers, consultancy for IT services and consulting firms, "
    "ai for companies whose product is AI/ML, general_startup otherwise. "
    "If a field cannot be verified from the pages, omit the company; never guess. "
)

SCOPE_RULES = {
    "local": EMPLOYER_RULES + (
        "Include a company only if it is headquartered in Ghana or has an office in Ghana; set ghana_eligibility to "
        "ghana_based, hq_location to its Ghana city, and evidence_url to a page showing the Ghana presence."
    ),
    "remote": EMPLOYER_RULES + (
        "Include a company only if it hires remote engineers and a page shows Ghana is an eligible hiring location: "
        "explicit_ghana if Ghana is named, africa_region if Africa or EMEA-wide remote, worldwide if hiring anywhere. "
        "Exclude companies whose remote roles are limited to the US, Europe or other regions that exclude Ghana. "
        "evidence_url must be that careers, job or remote-policy page, preferably on the company's own site or ATS."
    ),
}

# Never queue these: your current employer and anyone else you don't want contacted
EXCLUDED_EMPLOYERS = {"amalitech", "amalitech services gmbh"}


def role_of(company):
    return company["role_title"] or applicant.role_for(company["company_type"])


def recipient_name_of(contact):
    """Address a person by name; a departmental or generic inbox gets the team salutation."""
    if contact and contact["email_kind"] == "person" and contact["full_name"]:
        return contact["full_name"]
    return GENERIC_RECIPIENT


def letter_path_of(company):
    return os.path.join(LETTERS_DIR, applicant.letter_filename(company["name"]))


def site_resolves(url):
    try:
        res = requests.get(url, timeout=15, allow_redirects=True, stream=True,
                           headers={"User-Agent": "Mozilla/5.0"})
        res.close()
        return res.status_code < 500
    except requests.RequestException:
        return False


def run_exa_search(conn, query_str, scope="local"):
    """
    Searches for employers using Exa structured output and adds them to the database.
    scope 'local' finds Ghana-based firms; 'remote' finds remote firms that hire in Ghana.
    """
    from exa_search import ExaSearch
    print(f"[Pipeline] Executing Exa {scope} employer search for query: '{query_str}'...")
    exa = ExaSearch()
    companies = exa.find_employers(query_str, SCOPE_RULES[scope])

    added_count = 0
    for c in companies:
        name = c.get("name", "").strip()
        if not name or name.lower() in EXCLUDED_EMPLOYERS:
            continue
        if db.get_company_by_name(conn, name) or db.find_company_by_domain(conn, c.get("website", "")):
            continue
        careers_url = ""
        if scope == "remote":
            # Second check against the company's own careers pages before trusting remote eligibility
            v = exa.verify_remote_hiring(name, c.get("website", ""))
            if not v.get("ghana_eligible", "").startswith("yes"):
                print(f"[Pipeline] Skipping '{name}': Ghana eligibility {v.get('ghana_eligible')} - {v.get('note', '')}")
                continue
            c["website"] = v.get("official_website") or c.get("website", "")
            c["evidence_url"] = v.get("evidence_url") or c.get("evidence_url", "")
            c["ghana_eligibility"] = {"yes_named": "explicit_ghana", "yes_africa_or_emea": "africa_region",
                                      "yes_worldwide": "worldwide"}[v["ghana_eligible"]]
            careers_url = v.get("careers_url", "")
        parsed = urlparse(c.get("website", ""))
        if not parsed.netloc:
            print(f"[Pipeline] Skipping '{name}': no usable website.")
            continue
        website = f"{parsed.scheme or 'https'}://{parsed.netloc.lower()}"
        if not site_resolves(website):
            print(f"[Pipeline] Skipping '{name}': {website} did not respond.")
            continue

        ctype = c.get("company_type")
        if ctype not in COMPANY_TYPES:
            ctype = "general_startup"
        address = ""
        if scope == "local":
            address = c.get("hq_location") or "Ghana"
            if "ghana" not in address.lower():
                address = f"{address}, Ghana"

        _, created = db.upsert_company(
            conn, name,
            website=website,
            company_type=ctype,
            company_address=address,
            scope=scope,
            ghana_eligibility=c.get("ghana_eligibility", ""),
            evidence_url=c.get("evidence_url", ""),
            careers_url=careers_url,
        )
        if created:
            print(f"[Pipeline] Added company: {name}")
            added_count += 1

    print(f"[Pipeline] Exa search complete. Added {added_count} new companies (Exa cost: ${exa.total_cost:.3f}).")


def run_enrich(conn, limit=10, refresh=False, dry_run=False, company=None):
    from contact_enricher import ContactEnricher
    company_ids = None
    if company:
        row = db.get_company_by_name(conn, company)
        if not row:
            print(f"[Pipeline] No company named '{company}'.")
            return
        company_ids = [row["id"]]
    ContactEnricher(conn).run(limit=limit, company_ids=company_ids, refresh=refresh, dry_run=dry_run)


def run_review(conn, limit=None):
    import triage
    triage.run_review(conn, statuses=("Pending",), limit=limit)


def generate_letter(conn, company, contact):
    """Builds (or reuses) the grounded pitch and compiles the cover letter PDF. Returns (path, pitch)."""
    import llm_tailor
    from cover_letter_generator import CoverLetterGenerator
    os.makedirs(LETTERS_DIR, exist_ok=True)
    pitch = llm_tailor.ensure_pitch(conn, company["id"])
    path = letter_path_of(company)
    CoverLetterGenerator().generate_pdf(
        company_name=company["name"],
        role_title=role_of(company),
        company_type=company["company_type"],
        recipient_name=recipient_name_of(contact),
        company_address=company["company_address"] or "",
        output_path=path,
        pitch=pitch,
    )
    return path, pitch


def run_generate_letters(conn):
    """Compiles cover letters for Approved companies (the ones the next send will use)."""
    targets = db.list_companies(conn, "Approved")
    if not targets:
        print("[Pipeline] No Approved companies. Run 'review' first.")
        return
    print(f"[Pipeline] Generating cover letters for {len(targets)} companies...")
    for company in targets:
        generate_letter(conn, company, db.get_primary_contact(conn, company["id"]))
    print("[Pipeline] Cover letter generation complete.")


def run_send_emails(conn, limit=DAILY_SEND_LIMIT, dry_run=False):
    """
    Sends the first email to Approved companies with a primary contact, up to `limit` per run.
    Each send is recorded atomically with its Message-ID so follow-ups can thread onto it.
    """
    approved = db.list_companies(conn, "Approved")
    ready = []
    for company in approved:
        contact = db.get_primary_contact(conn, company["id"])
        if not contact:
            print(f"[Pipeline] '{company['name']}' has no primary contact; skipping (fix it in 'review').")
            continue
        if db.get_initial_outreach(conn, company["id"]):
            # Already emailed once; never send a second cold email
            print(f"[Pipeline] '{company['name']}' already has a sent initial email; marking Sent.")
            if not dry_run:
                db.set_company_status(conn, company["id"], "Sent")
            continue
        ready.append((company, contact))

    if not ready:
        print("[Pipeline] Nothing to send. Approve companies with 'review' first.")
        return

    to_send = ready[:limit]
    mode = "DRY-RUN" if dry_run else "LIVE"
    print(f"[Pipeline] {mode}: sending {len(to_send)} of {len(ready)} approved emails...")

    sender = None
    if not dry_run:
        from email_sender import EmailSender
        sender = EmailSender()

    sent_count = failed_count = 0
    for i, (company, contact) in enumerate(to_send):
        role = role_of(company)
        letter_path, pitch = generate_letter(conn, company, contact)
        highlights = [b["text"] for b in pitch.get("bullets", [])] or None
        body = applicant.outreach_body(company["name"], role, highlights=highlights)

        if dry_run:
            print(f"[DRY-RUN] Would email {contact['email']} ({recipient_name_of(contact)}) at {company['name']} "
                  f"- '{applicant.subject(role)}' with {os.path.basename(letter_path)}")
            continue

        # Re-read the status right before sending: the inbox checker or a review session may have changed it
        if db.get_company(conn, company["id"])["status"] != "Approved":
            print(f"[Pipeline] '{company['name']}' is no longer Approved; skipping.")
            continue

        result = sender.send_outreach_email(
            recipient_email=contact["email"],
            company_name=company["name"],
            cover_letter_path=letter_path,
            cv_path=CV_PATH,
            role_title=role,
            body=body,
        )
        ok = result["ok"]
        db.record_send(
            conn, company["id"], contact["id"], contact["email"], "initial",
            subject=result.get("subject"), message_id=result.get("message_id"),
            status="SUCCESS" if ok else "FAILED", error=result.get("error"),
            cover_letter_path=letter_path, new_company_status="Sent" if ok else "Failed",
        )
        if ok:
            sent_count += 1
        else:
            failed_count += 1

        # Random delay between emails (30 to 60 seconds) to stay clear of spam filters
        if i < len(to_send) - 1:
            delay = random.randint(30, 60)
            print(f"[Pipeline] Waiting {delay} seconds before sending next email...")
            time.sleep(delay)

    if not dry_run:
        print(f"[Pipeline] Run complete. Sent: {sent_count}, Failed: {failed_count}.")


def run_followups(conn, limit=10, dry_run=True):
    import followup_pipeline
    followup_pipeline.run_followups(conn=conn, limit=limit, dry_run=dry_run)


def run_check_replies(conn, days=None, dry_run=False, test_connection=False):
    import check_inbox
    if test_connection:
        ok = check_inbox.test_connection()
        sys.exit(0 if ok else 1)
    check_inbox.run_check(conn=conn, days=days, dry_run=dry_run)


def show_status(conn):
    """Prints live metrics from outreach.db."""
    s = db.status_counts(conn)
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError:
        Console = None

    if Console is None:
        print("\n--- Outreach Status ---")
        print(f"Companies: {s['total_companies']}")
        for status, n in s["companies"].items():
            print(f"  {status:<14} {n}")
        print(f"Contacts: {s['contacts']} ({s['person_contacts']} named people)")
        print(f"Emails sent: {s['outreaches_initial']} initial, {s['outreaches_followup']} follow-ups")
        print(f"Replies: {s['replies']}   Bounces: {s['bounces']}   Follow-ups due: {s['followups_due']}")
        print("-----------------------\n")
        return

    console = Console()
    companies = Table(title=f"Companies ({s['total_companies']})", show_header=True, header_style="bold")
    companies.add_column("Status")
    companies.add_column("Count", justify="right")
    for status, n in s["companies"].items():
        companies.add_row(status, str(n))

    activity = Table(title="Activity", show_header=True, header_style="bold")
    activity.add_column("Metric")
    activity.add_column("Value", justify="right")
    activity.add_row("Contacts", str(s["contacts"]))
    activity.add_row("Named decision-makers", str(s["person_contacts"]))
    activity.add_row("Initial emails", str(s["outreaches_initial"]))
    activity.add_row("Follow-ups sent", str(s["outreaches_followup"]))
    activity.add_row("Replies", str(s["replies"]))
    activity.add_row("Bounces", str(s["bounces"]))
    activity.add_row("Follow-ups due now", str(s["followups_due"]))

    console.print(companies)
    console.print(activity)


def build_parser():
    p = argparse.ArgumentParser(prog="outreach_pipeline.py", description="Job outreach engine (SQLite-backed).")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("search", help="Find employers with Exa and add them as Pending")
    s.add_argument("query", nargs="?", default="tech startup software development company Accra Ghana")
    s.add_argument("scope", nargs="?", default="local", choices=list(SCOPE_RULES))

    e = sub.add_parser("enrich", help="Find decision-maker contacts (Hunter -> Prospeo -> Apify)")
    e.add_argument("--limit", type=int, default=10)
    e.add_argument("--refresh", action="store_true", help="re-enrich companies that already have a person contact")
    e.add_argument("--dry-run", action="store_true")
    e.add_argument("--company", help="enrich a single company by name")

    r = sub.add_parser("review", help="Interactive review: approve, skip or edit Pending companies")
    r.add_argument("--limit", type=int)

    sub.add_parser("generate", help="Compile tailored cover letters for Approved companies")

    sd = sub.add_parser("send", help="Send first emails to Approved companies")
    sd.add_argument("--limit", type=int, default=DAILY_SEND_LIMIT)
    sd.add_argument("--dry-run", action="store_true")

    f = sub.add_parser("followup", help="Threaded follow-ups 6+ days after the first email (dry-run unless 'run')")
    f.add_argument("mode", nargs="?", choices=["run"], help="'run' sends for real")
    f.add_argument("--limit", type=int, default=10)

    c = sub.add_parser("check-replies", help="Scan the inbox for replies and bounces (read-only IMAP)")
    c.add_argument("--days", type=int)
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--test-connection", action="store_true")

    m = sub.add_parser("migrate", help="Import outreach_queue.csv and outreach_log.csv into outreach.db")
    m.add_argument("--dry-run", action="store_true")

    sub.add_parser("status", help="Show live metrics from outreach.db")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "migrate":
        import migrate_from_csv
        result = migrate_from_csv.migrate(dry_run=args.dry_run)
        sys.exit(0 if result["verified"] else 1)

    conn = db.connect()
    try:
        if args.cmd == "search":
            run_exa_search(conn, args.query, args.scope)
        elif args.cmd == "enrich":
            run_enrich(conn, limit=args.limit, refresh=args.refresh, dry_run=args.dry_run, company=args.company)
        elif args.cmd == "review":
            run_review(conn, limit=args.limit)
        elif args.cmd == "generate":
            run_generate_letters(conn)
        elif args.cmd == "send":
            run_send_emails(conn, limit=args.limit, dry_run=args.dry_run)
        elif args.cmd == "followup":
            run_followups(conn, limit=args.limit, dry_run=args.mode != "run")
        elif args.cmd == "check-replies":
            run_check_replies(conn, days=args.days, dry_run=args.dry_run, test_connection=args.test_connection)
        elif args.cmd == "status":
            show_status(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
