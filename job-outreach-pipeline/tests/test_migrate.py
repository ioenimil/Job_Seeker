import os
import csv
import sqlite3
import tempfile
import unittest

import db
import migrate_from_csv


class TestMigrate(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_migrate.db")
        self.queue_path = os.path.join(self.temp_dir.name, "test_queue.csv")
        self.log_path = os.path.join(self.temp_dir.name, "test_log.csv")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, filepath, rows, fieldnames):
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_migration_fixtures_followup_split_and_sent_without_log(self):
        """
        Tests migration logic with:
        - '| Followup:' date split producing both initial and followup outreaches
        - Sent-without-log synthesizing initial outreach from date_sent
        - Email kinds classified correctly
        - Generic recipient names excluded from contact full_name
        """
        queue_fields = [
            "company_name", "website", "email", "company_type", "recipient_name",
            "company_address", "status", "date_added", "date_sent", "scope",
            "ghana_eligibility", "evidence_url", "careers_url"
        ]
        queue_rows = [
            # Row 1: Followup split; generic recipient name
            {
                "company_name": "Company Alpha",
                "website": "https://alpha.com",
                "email": "careers@alpha.com",
                "company_type": "fintech",
                "recipient_name": "The Recruiting and Technology Team",
                "company_address": "Accra, Ghana",
                "status": "Sent",
                "date_added": "2026-10-01",
                "date_sent": "2026-10-01 10:00:00 | Followup: 2026-10-08 11:00:00",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://alpha.com",
                "careers_url": ""
            },
            # Row 2: Sent without log row; person recipient name
            {
                "company_name": "Company Beta",
                "website": "https://beta.com",
                "email": "kofi@beta.com",
                "company_type": "ai",
                "recipient_name": "Kofi Mensah",
                "company_address": "Kumasi, Ghana",
                "status": "Sent",
                "date_added": "2026-10-02",
                "date_sent": "2026-10-02 14:30:00",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://beta.com",
                "careers_url": ""
            },
            # Row 3: Skipped; unusable email
            {
                "company_name": "Company Gamma",
                "website": "https://gamma.com",
                "email": "no_email_found",
                "company_type": "fintech",
                "recipient_name": "The Hiring Team",
                "company_address": "Accra, Ghana",
                "status": "Skipped",
                "date_added": "2026-10-03",
                "date_sent": "",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://gamma.com",
                "careers_url": ""
            },
            # Row 4: Generic email kind
            {
                "company_name": "Company Delta",
                "website": "https://delta.com",
                "email": "info@delta.com",
                "company_type": "consultancy",
                "recipient_name": "Support Team",
                "company_address": "Accra, Ghana",
                "status": "Pending",
                "date_added": "2026-10-04",
                "date_sent": "",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://delta.com",
                "careers_url": ""
            }
        ]
        self.write_csv(self.queue_path, queue_rows, queue_fields)

        # Log row exists only for Company Alpha's initial send
        log_fields = ["date", "company_name", "email", "status", "cover_letter"]
        log_rows = [
            {
                "date": "2026-10-01 10:00:00",
                "company_name": "Company Alpha",
                "email": "careers@alpha.com",
                "status": "SUCCESS",
                "cover_letter": "Isaac_Obo_Enimil_Cover_Letter_Company_Alpha.pdf"
            }
        ]
        self.write_csv(self.log_path, log_rows, log_fields)

        result = migrate_from_csv.migrate(
            queue_path=self.queue_path,
            log_path=self.log_path,
            db_path=self.db_path,
            dry_run=False
        )

        self.assertTrue(result["verified"])
        self.assertEqual(result["companies_inserted"], 4)
        self.assertEqual(result["contacts_inserted"], 3)  # Alpha, Beta, Delta (Gamma had no_email_found)
        self.assertEqual(result["outreaches_inserted"], 3)  # Alpha initial, Alpha followup, Beta synthesized initial

        conn = db.connect(self.db_path)

        # Check Company Alpha: has 2 outreaches (initial + followup)
        c_alpha = db.get_company_by_name(conn, "Company Alpha")
        alpha_outreaches = db.list_outreaches(conn, c_alpha["id"])
        self.assertEqual(len(alpha_outreaches), 2)
        types = [o["email_type"] for o in alpha_outreaches]
        self.assertIn("initial", types)
        self.assertIn("followup", types)

        alpha_contact = db.get_primary_contact(conn, c_alpha["id"])
        self.assertIsNone(alpha_contact["full_name"])  # Generic recipient name filtered
        self.assertEqual(alpha_contact["email_kind"], "departmental")  # careers@

        # Check Company Beta: synthesized initial outreach
        c_beta = db.get_company_by_name(conn, "Company Beta")
        beta_outreaches = db.list_outreaches(conn, c_beta["id"])
        self.assertEqual(len(beta_outreaches), 1)
        self.assertEqual(beta_outreaches[0]["email_type"], "initial")
        self.assertEqual(beta_outreaches[0]["status"], "SUCCESS")
        self.assertEqual(beta_outreaches[0]["sent_at"], "2026-10-02 14:30:00")

        beta_contact = db.get_primary_contact(conn, c_beta["id"])
        self.assertEqual(beta_contact["full_name"], "Kofi Mensah")  # Person name preserved
        self.assertEqual(beta_contact["email_kind"], "person")

        # Check Company Delta: generic email
        c_delta = db.get_company_by_name(conn, "Company Delta")
        # info@ is stored, but a generic inbox is never made the primary
        self.assertIsNone(db.get_primary_contact(conn, c_delta["id"]))
        delta_contacts = db.list_contacts(conn, c_delta["id"])
        self.assertEqual([c["email_kind"] for c in delta_contacts], ["generic"])

        # Check Company Gamma: Skipped for lack of an email, tagged so enrichment can revive it
        c_gamma = db.get_company_by_name(conn, "Company Gamma")
        self.assertEqual(c_gamma["status"], "Skipped")
        self.assertEqual(c_gamma["notes"], "no_contact_found")
        self.assertIsNone(c_delta["notes"])

        conn.close()

    def test_migration_idempotency(self):
        """Running migration a second time results in 0 new inserts and passes verification."""
        queue_fields = ["company_name", "website", "email", "company_type", "recipient_name",
                        "company_address", "status", "date_added", "date_sent", "scope",
                        "ghana_eligibility", "evidence_url", "careers_url"]
        queue_rows = [
            {
                "company_name": "Idem Corp",
                "website": "https://idem.com",
                "email": "contact@idem.com",
                "company_type": "fintech",
                "recipient_name": "The Team",
                "company_address": "Accra",
                "status": "Sent",
                "date_added": "2026-10-05",
                "date_sent": "2026-10-05 12:00:00",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://idem.com",
                "careers_url": ""
            }
        ]
        self.write_csv(self.queue_path, queue_rows, queue_fields)

        log_fields = ["date", "company_name", "email", "status", "cover_letter"]
        log_rows = [
            {
                "date": "2026-10-05 12:00:00",
                "company_name": "Idem Corp",
                "email": "contact@idem.com",
                "status": "SUCCESS",
                "cover_letter": "Isaac_Obo_Enimil_Cover_Letter_Idem_Corp.pdf"
            }
        ]
        self.write_csv(self.log_path, log_rows, log_fields)

        # First run
        res1 = migrate_from_csv.migrate(
            queue_path=self.queue_path,
            log_path=self.log_path,
            db_path=self.db_path,
            dry_run=False
        )
        self.assertTrue(res1["verified"])
        self.assertEqual(res1["companies_inserted"], 1)
        self.assertEqual(res1["contacts_inserted"], 1)
        self.assertEqual(res1["outreaches_inserted"], 1)

        # Second run (should be a complete no-op)
        res2 = migrate_from_csv.migrate(
            queue_path=self.queue_path,
            log_path=self.log_path,
            db_path=self.db_path,
            dry_run=False
        )
        self.assertTrue(res2["verified"])
        self.assertEqual(res2["companies_inserted"], 0)
        self.assertEqual(res2["contacts_inserted"], 0)
        self.assertEqual(res2["outreaches_inserted"], 0)

    def test_no_status_downgrade(self):
        """Pre-existing company status (e.g. Replied) is never downgraded by migration (e.g. Sent)."""
        conn = db.connect(self.db_path)
        cid, _ = db.upsert_company(conn, "Protected Corp", status="Replied", website="https://protected.com")
        conn.close()

        # CSV specifies status="Sent"
        queue_fields = ["company_name", "website", "email", "company_type", "recipient_name",
                        "company_address", "status", "date_added", "date_sent", "scope",
                        "ghana_eligibility", "evidence_url", "careers_url"]
        queue_rows = [
            {
                "company_name": "Protected Corp",
                "website": "https://protected.com",
                "email": "ceo@protected.com",
                "company_type": "fintech",
                "recipient_name": "CEO",
                "company_address": "Accra",
                "status": "Sent",
                "date_added": "2026-10-06",
                "date_sent": "2026-10-06 12:00:00",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://protected.com",
                "careers_url": ""
            }
        ]
        self.write_csv(self.queue_path, queue_rows, queue_fields)
        self.write_csv(self.log_path, [], ["date", "company_name", "email", "status", "cover_letter"])

        migrate_from_csv.migrate(
            queue_path=self.queue_path,
            log_path=self.log_path,
            db_path=self.db_path,
            dry_run=False
        )

        conn = db.connect(self.db_path)
        comp = db.get_company(conn, cid)
        self.assertEqual(comp["status"], "Replied")  # Status remained 'Replied', not downgraded to 'Sent'
        conn.close()

    def test_dry_run_leaves_db_untouched(self):
        """Dry-run performs migration in a transaction then rolls back cleanly."""
        queue_fields = ["company_name", "website", "email", "company_type", "recipient_name",
                        "company_address", "status", "date_added", "date_sent", "scope",
                        "ghana_eligibility", "evidence_url", "careers_url"]
        queue_rows = [
            {
                "company_name": "DryRun Corp",
                "website": "https://dryrun.com",
                "email": "contact@dryrun.com",
                "company_type": "fintech",
                "recipient_name": "DryRun Team",
                "company_address": "Accra",
                "status": "Pending",
                "date_added": "2026-10-07",
                "date_sent": "",
                "scope": "local",
                "ghana_eligibility": "ghana_based",
                "evidence_url": "https://dryrun.com",
                "careers_url": ""
            }
        ]
        self.write_csv(self.queue_path, queue_rows, queue_fields)
        self.write_csv(self.log_path, [], ["date", "company_name", "email", "status", "cover_letter"])

        res = migrate_from_csv.migrate(
            queue_path=self.queue_path,
            log_path=self.log_path,
            db_path=self.db_path,
            dry_run=True
        )
        self.assertTrue(res["verified"])
        self.assertEqual(res["companies_inserted"], 1)

        conn = db.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
        self.assertEqual(count, 0)  # Rolled back!
        conn.close()


if __name__ == "__main__":
    unittest.main()
