import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta

import db


class TestDB(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_outreach.db")
        self.conn = db.connect(self.db_path)

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_schema_creation_idempotent(self):
        """init_db can be called multiple times without error and tracks user_version."""
        db.init_db(self.conn)
        db.init_db(self.conn)

        cur = self.conn.execute("PRAGMA user_version;")
        self.assertEqual(cur.fetchone()[0], 1)

        # Verify key tables exist
        tables = [
            row["name"] for row in self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        ]
        self.assertIn("companies", tables)
        self.assertIn("contacts", tables)
        self.assertIn("outreaches", tables)
        self.assertIn("inbox_events", tables)

    def test_upsert_dedupe_by_name(self):
        """upsert_company dedupes on name case-insensitively."""
        id1, created1 = db.upsert_company(self.conn, "Alpha Tech", website="https://alphatech.com")
        self.assertTrue(created1)

        id2, created2 = db.upsert_company(self.conn, "ALPHA TECH", website="https://other.com")
        self.assertFalse(created2)
        self.assertEqual(id1, id2)

    def test_upsert_dedupe_by_domain(self):
        """upsert_company dedupes on domain derived from website."""
        id1, created1 = db.upsert_company(self.conn, "Beta Holdings", website="https://betacorp.com")
        self.assertTrue(created1)

        id2, created2 = db.upsert_company(self.conn, "Beta Corp", website="https://www.betacorp.com/careers")
        self.assertFalse(created2)
        self.assertEqual(id1, id2)

    def test_fill_only_nulls(self):
        """On existing row, only fill columns that are currently NULL/'' — never overwrite set values."""
        id1, created = db.upsert_company(
            self.conn,
            "Gamma Inc",
            website="https://gamma.com",
            company_type="fintech",
            notes="Initial note",
            summary=None
        )
        self.assertTrue(created)

        # Attempt to overwrite existing fields, while filling summary
        id2, created2 = db.upsert_company(
            self.conn,
            "Gamma Inc",
            website="https://overwritten.com",
            company_type="ai",
            notes="New note",
            summary="Grounding summary text"
        )
        self.assertFalse(created2)
        self.assertEqual(id1, id2)

        row = db.get_company(self.conn, id1)
        self.assertEqual(row["website"], "https://gamma.com")
        self.assertEqual(row["company_type"], "fintech")
        self.assertEqual(row["notes"], "Initial note")
        self.assertEqual(row["summary"], "Grounding summary text")

    def test_status_validation(self):
        """Company status is validated against COMPANY_STATUSES."""
        # Upsert with invalid status
        with self.assertRaises(ValueError):
            db.upsert_company(self.conn, "Delta", status="InvalidStatus")

        cid, _ = db.upsert_company(self.conn, "Delta", status="Pending")

        # set_company_status with invalid status
        with self.assertRaises(ValueError):
            db.set_company_status(self.conn, cid, "NonExistentStatus")

        # update_company with invalid status
        with self.assertRaises(ValueError):
            db.update_company(self.conn, cid, status="BadStatus")

        # update_company with unknown column
        with self.assertRaises(ValueError):
            db.update_company(self.conn, cid, non_column="value")

        # Valid statuses
        db.set_company_status(self.conn, cid, "Approved")
        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Approved")

        db.set_company_status(self.conn, cid, "Apply-Online")
        row = db.get_company(self.conn, cid)
        self.assertEqual(row["status"], "Apply-Online")

    def test_one_primary_contact_invariant(self):
        """Partial unique index allows at most one primary contact per company; set_primary_contact is atomic."""
        cid, _ = db.upsert_company(self.conn, "Epsilon")

        ct1 = db.add_contact(self.conn, cid, "alice@epsilon.com", full_name="Alice", make_primary=True)
        primary = db.get_primary_contact(self.conn, cid)
        self.assertIsNotNone(primary)
        self.assertEqual(primary["id"], ct1)
        self.assertEqual(primary["is_primary"], 1)

        ct2 = db.add_contact(self.conn, cid, "bob@epsilon.com", full_name="Bob", make_primary=True)
        primary = db.get_primary_contact(self.conn, cid)
        self.assertEqual(primary["id"], ct2)
        self.assertEqual(primary["is_primary"], 1)

        # Ensure ct1 is no longer primary
        ct1_row = self.conn.execute("SELECT * FROM contacts WHERE id = ?", (ct1,)).fetchone()
        self.assertEqual(ct1_row["is_primary"], 0)

        # Directly inserting a second primary contact violates the partial unique index
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO contacts (company_id, email, is_primary) VALUES (?, 'charlie@epsilon.com', 1)",
                (cid,)
            )

        # Listing contacts returns primary first
        contacts = db.list_contacts(self.conn, cid)
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0]["id"], ct2)
        self.assertEqual(contacts[1]["id"], ct1)

    def test_record_send_atomicity(self):
        """record_send executes in ONE transaction and rolls back entirely on failure."""
        cid, _ = db.upsert_company(self.conn, "Zeta", status="Pending")
        ctid = db.add_contact(self.conn, cid, "contact@zeta.com")

        # Force failure mid-transaction by passing invalid new_company_status
        with self.assertRaises(ValueError):
            db.record_send(
                self.conn,
                company_id=cid,
                contact_id=ctid,
                recipient_email="contact@zeta.com",
                email_type="initial",
                subject="Test Subject",
                message_id="<msg-zeta-001@mail.com>",
                status="SUCCESS",
                new_company_status="InvalidStatus"
            )

        # Assert no outreach was persisted and company status was not updated
        outreaches = db.list_outreaches(self.conn, cid)
        self.assertEqual(len(outreaches), 0)
        company = db.get_company(self.conn, cid)
        self.assertEqual(company["status"], "Pending")

        # Test successful record_send
        oid = db.record_send(
            self.conn,
            company_id=cid,
            contact_id=ctid,
            recipient_email="contact@zeta.com",
            email_type="initial",
            subject="Test Subject",
            message_id="<msg-zeta-001@mail.com>",
            status="SUCCESS",
            new_company_status="Sent"
        )
        self.assertIsNotNone(oid)
        company = db.get_company(self.conn, cid)
        self.assertEqual(company["status"], "Sent")
        outreaches = db.list_outreaches(self.conn, cid)
        self.assertEqual(len(outreaches), 1)

    def test_followup_candidates_date_math_and_stop_statuses(self):
        """followup_candidates enforces date threshold, initial SUCCESS, and exclusion of STOP_STATUSES / replied / followups."""
        ref_now = datetime(2026, 10, 15, 12, 0, 0)

        # 1. Candidate: Sent 7 days ago, initial SUCCESS, no followup
        c1, _ = db.upsert_company(self.conn, "Candidate Corp", status="Sent")
        ct1 = db.add_contact(self.conn, c1, "lead@candidate.com", full_name="Lead One")
        db.record_send(
            self.conn, c1, ct1, "lead@candidate.com", "initial", "Subject",
            "<msg-1>", "SUCCESS", sent_at=(ref_now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        )

        # 2. Too early: Sent 3 days ago (< min_days=6)
        c2, _ = db.upsert_company(self.conn, "Early Corp", status="Sent")
        ct2 = db.add_contact(self.conn, c2, "lead@early.com", full_name="Lead Two")
        db.record_send(
            self.conn, c2, ct2, "lead@early.com", "initial", "Subject",
            "<msg-2>", "SUCCESS", sent_at=(ref_now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        )

        # 3. Replied (STOP_STATUSES): Sent 8 days ago
        c3, _ = db.upsert_company(self.conn, "Replied Corp", status="Replied")
        ct3 = db.add_contact(self.conn, c3, "lead@replied.com")
        db.record_send(
            self.conn, c3, ct3, "lead@replied.com", "initial", "Subject",
            "<msg-3>", "SUCCESS", sent_at=(ref_now - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        )

        # 4. Bounced (STOP_STATUSES): Sent 8 days ago
        c4, _ = db.upsert_company(self.conn, "Bounced Corp", status="Bounced")
        ct4 = db.add_contact(self.conn, c4, "lead@bounced.com")
        db.record_send(
            self.conn, c4, ct4, "lead@bounced.com", "initial", "Subject",
            "<msg-4>", "SUCCESS", sent_at=(ref_now - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        )

        # 5. Already sent SUCCESS followup: Sent 8 days ago
        c5, _ = db.upsert_company(self.conn, "Followed Up Corp", status="Sent")
        ct5 = db.add_contact(self.conn, c5, "lead@followed.com")
        db.record_send(
            self.conn, c5, ct5, "lead@followed.com", "initial", "Subject",
            "<msg-5a>", "SUCCESS", sent_at=(ref_now - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        )
        db.record_send(
            self.conn, c5, ct5, "lead@followed.com", "followup", "Re: Subject",
            "<msg-5b>", "SUCCESS", sent_at=(ref_now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        )

        # 6. Had FAILED followup (still a candidate): Sent 8 days ago
        c6, _ = db.upsert_company(self.conn, "Retry Followup Corp", status="Sent")
        ct6 = db.add_contact(self.conn, c6, "lead@retry.com", full_name="Retry Lead")
        db.record_send(
            self.conn, c6, ct6, "lead@retry.com", "initial", "Subject",
            "<msg-6a>", "SUCCESS", sent_at=(ref_now - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
        )
        db.record_send(
            self.conn, c6, ct6, "lead@retry.com", "followup", "Re: Subject",
            "<msg-6b>", "FAILED", sent_at=(ref_now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        )

        candidates = db.followup_candidates(self.conn, min_days=6, now=ref_now)
        cand_ids = [c["company_id"] for c in candidates]
        self.assertIn(c1, cand_ids)
        self.assertIn(c6, cand_ids)
        self.assertNotIn(c2, cand_ids)
        self.assertNotIn(c3, cand_ids)
        self.assertNotIn(c4, cand_ids)
        self.assertNotIn(c5, cand_ids)

        # Verify all required exposed fields exist on candidate row
        first = candidates[0]
        expected_keys = {
            "company_id", "company_name", "company_type", "role_title",
            "recipient_email", "contact_id", "full_name", "initial_outreach_id",
            "initial_message_id", "initial_subject", "initial_sent_at"
        }
        self.assertTrue(expected_keys.issubset(set(first.keys())))

    def test_inbox_event_idempotency(self):
        """record_inbox_event is idempotent on imap_message_id."""
        eid1, created1 = db.record_inbox_event(
            self.conn,
            kind="reply",
            from_email="founder@acme.com",
            imap_message_id="<imap-msg-1234@server.com>",
            subject="Interested in your CV"
        )
        self.assertTrue(created1)

        eid2, created2 = db.record_inbox_event(
            self.conn,
            kind="reply",
            from_email="founder@acme.com",
            imap_message_id="<imap-msg-1234@server.com>",
            subject="Interested in your CV"
        )
        self.assertFalse(created2)
        self.assertEqual(eid1, eid2)

        count = self.conn.execute("SELECT COUNT(*) FROM inbox_events").fetchone()[0]
        self.assertEqual(count, 1)

        # Invalid kind raises ValueError
        with self.assertRaises(ValueError):
            db.record_inbox_event(
                self.conn,
                kind="invalid_kind",
                from_email="a@b.com",
                imap_message_id="<imap-bad@server.com>"
            )

    def test_contact_validation_and_ranking(self):
        """Contact invalid emails raise ValueError; list_contacts ranks primary first then confidence desc."""
        cid, _ = db.upsert_company(self.conn, "Ranking Corp")

        with self.assertRaises(ValueError):
            db.add_contact(self.conn, cid, "")
        with self.assertRaises(ValueError):
            db.add_contact(self.conn, cid, "no_email_found")
        with self.assertRaises(ValueError):
            db.add_contact(self.conn, cid, "notanemail")

        # Contact 1: non-primary, confidence 90
        ct1 = db.add_contact(self.conn, cid, "c1@ranking.com", confidence_score=90)
        # Contact 2: primary, confidence 50
        ct2 = db.add_contact(self.conn, cid, "c2@ranking.com", confidence_score=50, make_primary=True)
        # Contact 3: non-primary, confidence 95
        ct3 = db.add_contact(self.conn, cid, "c3@ranking.com", confidence_score=95)

        contacts = db.list_contacts(self.conn, cid)
        # Primary first (ct2), then highest confidence (ct3 with 95, ct1 with 90)
        self.assertEqual([c["id"] for c in contacts], [ct2, ct3, ct1])

        # find_contact_by_email includes company columns
        found = db.find_contact_by_email(self.conn, "c2@ranking.com")
        self.assertIsNotNone(found)
        self.assertEqual(found["company_name"], "Ranking Corp")
        self.assertEqual(found["company_status"], "Pending")

    def test_status_counts(self):
        """status_counts returns complete statistics dict matching spec."""
        c1, _ = db.upsert_company(self.conn, "Count Corp 1", status="Sent")
        c2, _ = db.upsert_company(self.conn, "Count Corp 2", status="Skipped")

        db.add_contact(self.conn, c1, "lead@count1.com", email_kind="person")
        db.add_contact(self.conn, c2, "info@count2.com", email_kind="generic")

        counts = db.status_counts(self.conn)
        self.assertEqual(counts["total_companies"], 2)
        self.assertEqual(counts["contacts"], 2)
        self.assertEqual(counts["person_contacts"], 1)
        self.assertEqual(counts["companies"]["Sent"], 1)
        self.assertEqual(counts["companies"]["Skipped"], 1)
        self.assertEqual(counts["companies"]["Pending"], 0)


if __name__ == "__main__":
    unittest.main()
