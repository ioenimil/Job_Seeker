import os
import sqlite3
import urllib.parse
from datetime import datetime, timedelta
from contextlib import contextmanager
from config import config

DB_PATH = config.get("OUTREACH_DB") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach.db")

COMPANY_STATUSES = (
    "Pending", "Approved", "Sent", "Followup-Sent", "Replied", "Bounced", "Skipped",
    "Failed", "Apply-Online"
)
CONTACT_SOURCES = ("hunter", "prospeo", "apify", "manual")
EMAIL_KINDS = ("person", "departmental", "generic")
VERIFICATION = ("valid", "invalid", "accept_all", "unknown")
EMAIL_TYPES = ("initial", "followup")
OUTREACH_STATUSES = ("SUCCESS", "FAILED")
INBOX_EVENT_KINDS = ("reply", "bounce", "auto_reply", "unsubscribe")
STOP_STATUSES = ("Replied", "Bounced")

COMPANY_UPDATABLE_COLUMNS = {
    "name", "website", "domain", "company_type", "company_address",
    "scope", "ghana_eligibility", "evidence_url", "careers_url",
    "summary", "role_title", "pitch", "notes", "status"
}


def now_iso():
    """Returns local timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def bare_domain(url):
    """Returns lowercase netloc without 'www.' (accepts 'example.com' without scheme too)."""
    if not url:
        return ""
    url = url.strip()
    if not url:
        return ""
    if "://" not in url:
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    netloc = parsed.netloc or parsed.path.split("/")[0]
    netloc = netloc.split(":")[0].lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


_sp_counter = 0


@contextmanager
def transaction(conn):
    """Context manager: BEGIN IMMEDIATE ... COMMIT, ROLLBACK on exception (re-raise). Supports nesting via SAVEPOINT."""
    global _sp_counter
    if not conn.in_transaction:
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield conn
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
    else:
        _sp_counter += 1
        sp_name = f"sp_{_sp_counter}"
        conn.execute(f"SAVEPOINT {sp_name}")
        try:
            yield conn
            conn.execute(f"RELEASE SAVEPOINT {sp_name}")
        except Exception:
            conn.execute(f"ROLLBACK TO SAVEPOINT {sp_name}")
            conn.execute(f"RELEASE SAVEPOINT {sp_name}")
            raise


def init_db(conn):
    """Idempotent CREATE TABLE/INDEX IF NOT EXISTS; tracks version in PRAGMA user_version."""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE COLLATE NOCASE,
        website TEXT,
        domain TEXT,
        company_type TEXT,
        company_address TEXT,
        scope TEXT,
        ghana_eligibility TEXT,
        evidence_url TEXT,
        careers_url TEXT,
        summary TEXT,
        role_title TEXT,
        pitch TEXT,
        notes TEXT,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Sent', 'Followup-Sent', 'Replied', 'Bounced', 'Skipped', 'Failed', 'Apply-Online')),
        created_at TEXT,
        updated_at TEXT
    );
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_companies_domain ON companies(domain);")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
        full_name TEXT,
        title TEXT,
        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
        source TEXT CHECK(source IS NULL OR source IN ('hunter', 'prospeo', 'apify', 'manual')),
        confidence_score INTEGER,
        verification_status TEXT CHECK(verification_status IS NULL OR verification_status IN ('valid', 'invalid', 'accept_all', 'unknown')),
        email_kind TEXT CHECK(email_kind IS NULL OR email_kind IN ('person', 'departmental', 'generic')),
        is_primary INTEGER NOT NULL DEFAULT 0 CHECK(is_primary IN (0, 1)),
        created_at TEXT,
        updated_at TEXT
    );
    """)

    conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_primary
    ON contacts(company_id)
    WHERE is_primary = 1;
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS outreaches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL REFERENCES companies(id),
        contact_id INTEGER REFERENCES contacts(id),
        recipient_email TEXT NOT NULL,
        email_type TEXT NOT NULL CHECK(email_type IN ('initial', 'followup')),
        subject TEXT,
        message_id TEXT UNIQUE,
        in_reply_to TEXT,
        references_header TEXT,
        status TEXT NOT NULL CHECK(status IN ('SUCCESS', 'FAILED')),
        error TEXT,
        sent_at TEXT NOT NULL,
        cover_letter_path TEXT,
        UNIQUE(company_id, recipient_email, email_type, sent_at)
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS inbox_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL CHECK(kind IN ('reply', 'bounce', 'auto_reply', 'unsubscribe')),
        from_email TEXT,
        subject TEXT,
        imap_message_id TEXT NOT NULL UNIQUE,
        received_at TEXT,
        snippet TEXT,
        company_id INTEGER REFERENCES companies(id),
        contact_id INTEGER REFERENCES contacts(id),
        outreach_id INTEGER REFERENCES outreaches(id),
        created_at TEXT
    );
    """)

    cur = conn.execute("PRAGMA user_version;")
    row = cur.fetchone()
    version = row[0] if row else 0
    if version < 1:
        conn.execute("PRAGMA user_version = 1;")
        version = 1
    if version < 2:
        # v2: keep the exact body of every email so follow-ups can quote what was really sent
        columns = {r["name"] if isinstance(r, sqlite3.Row) else r[1] for r in conn.execute("PRAGMA table_info(outreaches)")}
        if "body" not in columns:
            conn.execute("ALTER TABLE outreaches ADD COLUMN body TEXT")
        conn.execute("PRAGMA user_version = 2;")


def connect(db_path=None):
    """
    Connect to SQLite DB:
    row_factory=sqlite3.Row; PRAGMA foreign_keys=ON; journal_mode=WAL; busy_timeout=5000;
    isolation_level=None (autocommit; use transaction() for multi-statement writes); calls init_db().
    """
    if db_path is None:
        db_path = DB_PATH
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    init_db(conn)
    return conn


def upsert_company(conn, name, **fields):
    """
    Dedupe on name (case-insensitive) OR on domain (derived from website).
    On existing row, only fill columns that are currently NULL/'' — never overwrite set values, never change status.
    Returns (company_id, created: bool).
    """
    name = (name or "").strip()
    if not name:
        raise ValueError("Company name cannot be empty")

    domain = fields.get("domain")
    website = fields.get("website")
    if not domain and website:
        domain = bare_domain(website)
    elif domain:
        domain = bare_domain(domain)

    # 1. Dedupe on name (case-insensitive) OR on domain
    row = conn.execute("SELECT * FROM companies WHERE lower(name) = lower(?)", (name,)).fetchone()
    if not row and domain:
        row = conn.execute(
            "SELECT * FROM companies WHERE domain = ? AND domain IS NOT NULL AND domain != ''",
            (domain,)
        ).fetchone()

    if row:
        company_id = row["id"]
        allowed_cols = [
            "website", "domain", "company_type", "company_address", "scope",
            "ghana_eligibility", "evidence_url", "careers_url", "summary",
            "role_title", "pitch", "notes"
        ]
        updates = {}
        candidate_values = dict(fields)
        if domain:
            candidate_values["domain"] = domain
        for col in allowed_cols:
            if col in candidate_values:
                val = candidate_values[col]
                curr_val = row[col]
                if (curr_val is None or curr_val == "") and (val is not None and val != ""):
                    updates[col] = val

        if updates:
            updates["updated_at"] = now_iso()
            set_clauses = [f"{col} = ?" for col in updates]
            params = list(updates.values()) + [company_id]
            conn.execute(f"UPDATE companies SET {', '.join(set_clauses)} WHERE id = ?", params)

        return company_id, False
    else:
        status = fields.get("status", "Pending")
        if status not in COMPANY_STATUSES:
            raise ValueError(f"Invalid company status: {status}")

        created_at = fields.get("created_at") or now_iso()
        updated_at = fields.get("updated_at") or now_iso()

        cols = ["name", "status", "created_at", "updated_at"]
        vals = [name, status, created_at, updated_at]

        if domain:
            cols.append("domain")
            vals.append(domain)

        optional_cols = [
            "website", "company_type", "company_address", "scope",
            "ghana_eligibility", "evidence_url", "careers_url",
            "summary", "role_title", "pitch", "notes"
        ]
        for col in optional_cols:
            if col in fields and fields[col] is not None:
                cols.append(col)
                vals.append(fields[col])

        placeholders = ", ".join("?" for _ in cols)
        col_names = ", ".join(cols)
        cur = conn.execute(f"INSERT INTO companies ({col_names}) VALUES ({placeholders})", vals)
        return cur.lastrowid, True


def get_company(conn, company_id):
    """Fetch company by id. Returns Row | None."""
    return conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()


def get_company_by_name(conn, name):
    """Fetch company by name (case-insensitive). Returns Row | None."""
    if not name:
        return None
    return conn.execute("SELECT * FROM companies WHERE lower(name) = lower(?)", (name.strip(),)).fetchone()


def find_company_by_domain(conn, domain_or_url):
    """Fetch company by domain or url. Returns Row | None."""
    domain = bare_domain(domain_or_url)
    if not domain:
        return None
    return conn.execute("SELECT * FROM companies WHERE domain = ? LIMIT 1", (domain,)).fetchone()


def list_companies(conn, statuses=None, order_by="id"):
    """
    List companies optionally filtered by statuses (str or iterable).
    Order by whitelisted column (default 'id'). Returns list[Row].
    """
    allowed_order_by = {"id", "name", "created_at", "updated_at", "status", "domain"}
    order_col = order_by.lower().strip()
    if order_col not in allowed_order_by:
        raise ValueError(f"Invalid order_by column: {order_by}")

    if statuses is None:
        return conn.execute(f"SELECT * FROM companies ORDER BY {order_col} ASC").fetchall()
    elif isinstance(statuses, str):
        return conn.execute(f"SELECT * FROM companies WHERE status = ? ORDER BY {order_col} ASC", (statuses,)).fetchall()
    else:
        status_list = list(statuses)
        if not status_list:
            return []
        placeholders = ",".join("?" for _ in status_list)
        return conn.execute(f"SELECT * FROM companies WHERE status IN ({placeholders}) ORDER BY {order_col} ASC", status_list).fetchall()


def update_company(conn, company_id, **fields):
    """
    Update company fields (whitelisted columns only; ValueError on unknown; bumps updated_at).
    """
    if not fields:
        return
    for k in fields:
        if k not in COMPANY_UPDATABLE_COLUMNS:
            raise ValueError(f"Unknown or non-updatable column: {k}")

    if "status" in fields:
        if fields["status"] not in COMPANY_STATUSES:
            raise ValueError(f"Invalid company status: {fields['status']}")

    fields_to_set = dict(fields)
    if "website" in fields_to_set and "domain" not in fields_to_set:
        fields_to_set["domain"] = bare_domain(fields_to_set["website"])
    elif "domain" in fields_to_set:
        fields_to_set["domain"] = bare_domain(fields_to_set["domain"])

    fields_to_set["updated_at"] = now_iso()
    set_clauses = [f"{col} = ?" for col in fields_to_set]
    params = list(fields_to_set.values()) + [company_id]
    cur = conn.execute(f"UPDATE companies SET {', '.join(set_clauses)} WHERE id = ?", params)
    if cur.rowcount == 0:
        raise ValueError(f"Company {company_id} not found")


def set_company_status(conn, company_id, status):
    """Validates against COMPANY_STATUSES; bumps updated_at."""
    if status not in COMPANY_STATUSES:
        raise ValueError(f"Invalid company status: {status}")
    cur = conn.execute(
        "UPDATE companies SET status = ?, updated_at = ? WHERE id = ?",
        (status, now_iso(), company_id)
    )
    if cur.rowcount == 0:
        raise ValueError(f"Company {company_id} not found")


def add_contact(conn, company_id, email, full_name=None, title=None, source="manual",
                confidence_score=None, verification_status=None, email_kind=None,
                make_primary=False):
    """
    Upsert on email (case-insensitive, stored lowercased+stripped).
    On existing email: fill NULL fields, keep the higher confidence_score.
    If make_primary: set_primary_contact in the same transaction.
    Reject obviously invalid emails (no "@", "no_email_found", empty) with ValueError.
    Returns contact_id.
    """
    if not email or not isinstance(email, str):
        raise ValueError("Invalid email: empty or non-string")
    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean or email_clean == "no_email_found":
        raise ValueError(f"Invalid email: {email}")

    if source is not None and source not in CONTACT_SOURCES:
        raise ValueError(f"Invalid contact source: {source}")
    if verification_status is not None and verification_status not in VERIFICATION:
        raise ValueError(f"Invalid verification status: {verification_status}")
    if email_kind is not None and email_kind not in EMAIL_KINDS:
        raise ValueError(f"Invalid email kind: {email_kind}")

    with transaction(conn):
        row = conn.execute("SELECT * FROM contacts WHERE lower(email) = lower(?)", (email_clean,)).fetchone()
        if row:
            contact_id = row["id"]
            updates = {}
            if (row["full_name"] is None or row["full_name"] == "") and full_name:
                updates["full_name"] = full_name
            if (row["title"] is None or row["title"] == "") and title:
                updates["title"] = title
            if row["source"] is None and source:
                updates["source"] = source
            if row["verification_status"] is None and verification_status:
                updates["verification_status"] = verification_status
            if row["email_kind"] is None and email_kind:
                updates["email_kind"] = email_kind

            old_conf = row["confidence_score"]
            if confidence_score is not None:
                if old_conf is None or confidence_score > old_conf:
                    updates["confidence_score"] = confidence_score

            if updates:
                updates["updated_at"] = now_iso()
                set_clauses = [f"{col} = ?" for col in updates]
                params = list(updates.values()) + [contact_id]
                conn.execute(f"UPDATE contacts SET {', '.join(set_clauses)} WHERE id = ?", params)
        else:
            now = now_iso()
            cur = conn.execute(
                """INSERT INTO contacts (
                    company_id, full_name, title, email, source,
                    confidence_score, verification_status, email_kind,
                    is_primary, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)""",
                (company_id, full_name, title, email_clean, source,
                 confidence_score, verification_status, email_kind, now, now)
            )
            contact_id = cur.lastrowid

        if make_primary:
            set_primary_contact(conn, company_id, contact_id)

        return contact_id


def set_primary_contact(conn, company_id, contact_id):
    """Atomically clears the old primary and sets the new primary contact."""
    with transaction(conn):
        now = now_iso()
        conn.execute(
            "UPDATE contacts SET is_primary = 0, updated_at = ? WHERE company_id = ? AND is_primary = 1",
            (now, company_id)
        )
        cur = conn.execute(
            "UPDATE contacts SET is_primary = 1, updated_at = ? WHERE id = ? AND company_id = ?",
            (now, contact_id, company_id)
        )
        if cur.rowcount == 0:
            raise ValueError(f"Contact {contact_id} not found for company {company_id}")


def get_primary_contact(conn, company_id):
    """Returns primary contact Row | None for the given company."""
    return conn.execute(
        "SELECT * FROM contacts WHERE company_id = ? AND is_primary = 1 LIMIT 1",
        (company_id,)
    ).fetchone()


def list_contacts(conn, company_id):
    """Lists contacts for company: primary first, then confidence desc."""
    return conn.execute(
        """SELECT * FROM contacts
        WHERE company_id = ?
        ORDER BY is_primary DESC, confidence_score DESC NULLS LAST, id ASC""",
        (company_id,)
    ).fetchall()


def find_contact_by_email(conn, email):
    """Find contact by email (case-insensitive). Includes company columns: company_name, company_status."""
    if not email:
        return None
    return conn.execute(
        """SELECT c.*, comp.name AS company_name, comp.status AS company_status
        FROM contacts c
        JOIN companies comp ON c.company_id = comp.id
        WHERE lower(c.email) = lower(?)
        LIMIT 1""",
        (email.strip(),)
    ).fetchone()


def record_send(conn, company_id, contact_id, recipient_email, email_type, subject, message_id, status,
                in_reply_to=None, references=None, cover_letter_path=None, error=None, sent_at=None,
                new_company_status=None, body=None):
    """
    ONE transaction: insert outreach row; if new_company_status given, set the company status too.
    Returns outreach_id.
    """
    if email_type not in EMAIL_TYPES:
        raise ValueError(f"Invalid email type: {email_type}")
    if status not in OUTREACH_STATUSES:
        raise ValueError(f"Invalid outreach status: {status}")
    if new_company_status is not None and new_company_status not in COMPANY_STATUSES:
        raise ValueError(f"Invalid company status: {new_company_status}")

    sent_at = sent_at or now_iso()
    recipient_email = recipient_email.strip().lower()

    with transaction(conn):
        cur = conn.execute(
            """INSERT INTO outreaches (
                company_id, contact_id, recipient_email, email_type, subject,
                message_id, in_reply_to, references_header, status, error,
                sent_at, cover_letter_path, body
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (company_id, contact_id, recipient_email, email_type, subject,
             message_id, in_reply_to, references, status, error,
             sent_at, cover_letter_path, body)
        )
        outreach_id = cur.lastrowid
        if new_company_status is not None:
            set_company_status(conn, company_id, new_company_status)
        return outreach_id


def get_initial_outreach(conn, company_id):
    """Returns latest SUCCESS initial outreach Row | None."""
    return conn.execute(
        """SELECT * FROM outreaches
        WHERE company_id = ? AND email_type = 'initial' AND status = 'SUCCESS'
        ORDER BY sent_at DESC, id DESC
        LIMIT 1""",
        (company_id,)
    ).fetchone()


def list_outreaches(conn, company_id=None):
    """Lists outreaches for company_id, or all outreaches if company_id is None."""
    if company_id is not None:
        return conn.execute(
            "SELECT * FROM outreaches WHERE company_id = ? ORDER BY sent_at ASC, id ASC",
            (company_id,)
        ).fetchall()
    return conn.execute(
        "SELECT * FROM outreaches ORDER BY sent_at ASC, id ASC"
    ).fetchall()


def followup_candidates(conn, min_days=6, now=None):
    """
    Companies with status 'Sent' that have a SUCCESS initial outreach sent <= now - min_days,
    no SUCCESS followup yet, and status not in STOP_STATUSES.
    Each row exposes: company_id, company_name, company_type, role_title, recipient_email,
    contact_id, full_name, initial_outreach_id, initial_message_id, initial_subject, initial_sent_at,
    initial_body (NULL for sends made before schema v2).
    """
    if now is None:
        now_dt = datetime.now()
    elif isinstance(now, str):
        try:
            now_dt = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            now_dt = datetime.strptime(now, "%Y-%m-%d")
    elif isinstance(now, datetime):
        now_dt = now
    else:
        raise ValueError(f"Invalid now format: {now}")

    cutoff = (now_dt - timedelta(days=min_days)).strftime("%Y-%m-%d %H:%M:%S")

    return conn.execute(
        """SELECT
            comp.id AS company_id,
            comp.name AS company_name,
            comp.company_type AS company_type,
            comp.role_title AS role_title,
            o.recipient_email AS recipient_email,
            o.contact_id AS contact_id,
            cont.full_name AS full_name,
            o.id AS initial_outreach_id,
            o.message_id AS initial_message_id,
            o.subject AS initial_subject,
            o.sent_at AS initial_sent_at,
            o.body AS initial_body
        FROM companies comp
        JOIN outreaches o ON o.id = (
            SELECT o2.id FROM outreaches o2
            WHERE o2.company_id = comp.id
              AND o2.email_type = 'initial'
              AND o2.status = 'SUCCESS'
            ORDER BY o2.sent_at DESC, o2.id DESC
            LIMIT 1
        )
        LEFT JOIN contacts cont ON o.contact_id = cont.id
        WHERE comp.status = 'Sent'
          AND comp.status NOT IN ('Replied', 'Bounced')
          AND o.sent_at <= ?
          AND NOT EXISTS (
              SELECT 1 FROM outreaches f
              WHERE f.company_id = comp.id
                AND f.email_type = 'followup'
                AND f.status = 'SUCCESS'
          )
        ORDER BY o.sent_at ASC, comp.id ASC""",
        (cutoff,)
    ).fetchall()


def record_inbox_event(conn, kind, from_email, imap_message_id, subject=None, received_at=None,
                       snippet=None, company_id=None, contact_id=None, outreach_id=None):
    """
    Records an inbox event. Idempotent on imap_message_id.
    Returns (event_id, created: bool).
    """
    if kind not in INBOX_EVENT_KINDS:
        raise ValueError(f"Invalid inbox event kind: {kind}")

    with transaction(conn):
        row = conn.execute(
            "SELECT id FROM inbox_events WHERE imap_message_id = ?",
            (imap_message_id,)
        ).fetchone()
        if row:
            return row["id"], False

        now = now_iso()
        rec_at = received_at or now
        cur = conn.execute(
            """INSERT INTO inbox_events (
                kind, from_email, subject, imap_message_id, received_at,
                snippet, company_id, contact_id, outreach_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (kind, from_email, subject, imap_message_id, rec_at,
             snippet, company_id, contact_id, outreach_id, now)
        )
        return cur.lastrowid, True


def set_outreach_message_id(conn, outreach_id, message_id):
    """Backfills outreach message_id for legacy rows."""
    conn.execute(
        "UPDATE outreaches SET message_id = ? WHERE id = ?",
        (message_id, outreach_id)
    )


def status_counts(conn):
    """
    Returns dict:
    {"companies": {status: n, ...}, "total_companies", "contacts",
     "person_contacts", "outreaches_initial", "outreaches_followup",
     "replies", "bounces", "followups_due"}
    """
    comp_counts = {s: 0 for s in COMPANY_STATUSES}
    for row in conn.execute("SELECT status, COUNT(*) AS cnt FROM companies GROUP BY status").fetchall():
        comp_counts[row["status"]] = row["cnt"]

    total_companies = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_contacts = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    person_contacts = conn.execute("SELECT COUNT(*) FROM contacts WHERE email_kind = 'person'").fetchone()[0]
    outreaches_initial = conn.execute("SELECT COUNT(*) FROM outreaches WHERE email_type = 'initial'").fetchone()[0]
    outreaches_followup = conn.execute("SELECT COUNT(*) FROM outreaches WHERE email_type = 'followup'").fetchone()[0]
    replies = conn.execute("SELECT COUNT(*) FROM inbox_events WHERE kind = 'reply'").fetchone()[0]
    bounces = conn.execute("SELECT COUNT(*) FROM inbox_events WHERE kind = 'bounce'").fetchone()[0]
    followups_due = len(followup_candidates(conn))

    return {
        "companies": comp_counts,
        "total_companies": total_companies,
        "contacts": total_contacts,
        "person_contacts": person_contacts,
        "outreaches_initial": outreaches_initial,
        "outreaches_followup": outreaches_followup,
        "replies": replies,
        "bounces": bounces,
        "followups_due": followups_due,
    }
