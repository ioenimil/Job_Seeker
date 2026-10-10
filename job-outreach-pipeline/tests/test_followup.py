import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os
import shutil
from datetime import datetime, timedelta

import db
import applicant
from followup_pipeline import run_followups


class TestFollowupPipeline(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_followup.db")
        self.conn = db.connect(self.db_path)

        # 7 days ago
        now = datetime.now()
        self.sent_7d_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        self.sent_2d_ago = (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        # 1. Alpha Tech: Sent 7 days ago with message_id -> due
        self.c1_id, _ = db.upsert_company(self.conn, "Alpha Tech", website="https://alphatech.com", status="Sent", company_type="ai")
        self.cont1_id = db.add_contact(self.conn, self.c1_id, "recruiter@alphatech.com", full_name="Alice Recruiter", make_primary=True)
        db.record_send(
            self.conn, self.c1_id, self.cont1_id, "recruiter@alphatech.com",
            email_type="initial", subject="Forward Deployed Engineer Application - Isaac Obo Enimil",
            message_id="<orig-alpha@alphatech.com>", status="SUCCESS", sent_at=self.sent_7d_ago
        )

        # 2. Beta Inc: Sent 7 days ago with NULL message_id -> due (legacy)
        self.c2_id, _ = db.upsert_company(self.conn, "Beta Inc", website="https://betainc.com", status="Sent", company_type="consultancy")
        self.cont2_id = db.add_contact(self.conn, self.c2_id, "jobs@betainc.com", full_name="Bob Hiring", make_primary=True)
        db.record_send(
            self.conn, self.c2_id, self.cont2_id, "jobs@betainc.com",
            email_type="initial", subject="Forward Deployed / Platform Engineer Application - Isaac Obo Enimil",
            message_id=None, status="SUCCESS", sent_at=self.sent_7d_ago
        )

        # 3. Gamma Corp: Sent 7 days ago, but status='Replied' -> excluded
        self.c3_id, _ = db.upsert_company(self.conn, "Gamma Corp", website="https://gammacorp.com", status="Replied")
        self.cont3_id = db.add_contact(self.conn, self.c3_id, "hr@gammacorp.com", make_primary=True)
        db.record_send(
            self.conn, self.c3_id, self.cont3_id, "hr@gammacorp.com",
            email_type="initial", subject="Application", message_id="<orig-gamma@gamma.com>",
            status="SUCCESS", sent_at=self.sent_7d_ago
        )

        # 4. Delta LLC: Sent 7 days ago, but status='Bounced' -> excluded
        self.c4_id, _ = db.upsert_company(self.conn, "Delta LLC", website="https://deltallc.com", status="Bounced")
        self.cont4_id = db.add_contact(self.conn, self.c4_id, "hr@deltallc.com", make_primary=True)
        db.record_send(
            self.conn, self.c4_id, self.cont4_id, "hr@deltallc.com",
            email_type="initial", subject="Application", message_id="<orig-delta@delta.com>",
            status="SUCCESS", sent_at=self.sent_7d_ago
        )

        # 5. Epsilon AI: Sent 2 days ago -> excluded (not min_days)
        self.c5_id, _ = db.upsert_company(self.conn, "Epsilon AI", website="https://epsilon.ai", status="Sent")
        self.cont5_id = db.add_contact(self.conn, self.c5_id, "hr@epsilon.ai", make_primary=True)
        db.record_send(
            self.conn, self.c5_id, self.cont5_id, "hr@epsilon.ai",
            email_type="initial", subject="Application", message_id="<orig-epsilon@epsilon.ai>",
            status="SUCCESS", sent_at=self.sent_2d_ago
        )

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.test_dir)

    def test_followup_candidates_excludes_replied_bounced_recent(self):
        candidates = db.followup_candidates(self.conn, min_days=6)
        company_names = [c["company_name"] for c in candidates]
        self.assertIn("Alpha Tech", company_names)
        self.assertIn("Beta Inc", company_names)
        self.assertNotIn("Gamma Corp", company_names)
        self.assertNotIn("Delta LLC", company_names)
        self.assertNotIn("Epsilon AI", company_names)
        self.assertEqual(len(candidates), 2)

    @patch("time.sleep")
    @patch("check_inbox.run_check")
    @patch("followup_pipeline.EmailSender")
    def test_followup_quotes_the_stored_original_and_greets_by_name(self, mock_sender_cls, mock_run_check, mock_sleep):
        """The follow-up quotes the body the recipient actually got; legacy sends without a stored body quote nothing."""
        original = "Dear Alice,\n\nMy name is Isaac.\n\nThanks for reading."
        self.conn.execute("UPDATE outreaches SET body = ? WHERE company_id = ? AND email_type = 'initial'",
                          (original, self.c1_id))
        mock_sender = MagicMock()
        mock_sender.sender_email = "test@example.com"
        mock_sender.send_followup.side_effect = lambda **kw: {
            "ok": True, "message_id": f"<f-{kw['recipient_email']}>", "subject": kw["subject"], "error": None}
        mock_sender_cls.return_value = mock_sender

        run_followups(conn=self.conn, limit=10, dry_run=False, check_inbox_first=True)

        bodies = {c.kwargs["recipient_email"]: c.kwargs["body"] for c in mock_sender.send_followup.call_args_list}
        alpha = bodies["recruiter@alphatech.com"]
        self.assertTrue(alpha.startswith("Dear Alice,"))
        self.assertIn("wrote:\n> Dear Alice,\n>\n> My name is Isaac.", alpha)
        self.assertNotIn("wrote:", bodies["jobs@betainc.com"])
        stored = [o for o in db.list_outreaches(self.conn, self.c1_id) if o["email_type"] == "followup"][0]
        self.assertEqual(stored["body"], alpha)

    @patch("time.sleep")
    @patch("check_inbox.run_check")
    @patch("followup_pipeline.EmailSender")
    def test_followup_live_run_sends_and_records_per_send(self, mock_sender_cls, mock_run_check, mock_sleep):
        mock_sender = MagicMock()
        mock_sender.sender_email = "test@example.com"
        mock_sender_cls.return_value = mock_sender

        def fake_send_followup(recipient_email, subject, body, in_reply_to, references, attachments=()):
            return {
                "ok": True,
                "message_id": f"<new-followup-{recipient_email}>",
                "subject": subject,
                "error": None
            }
        mock_sender.send_followup.side_effect = fake_send_followup

        res = run_followups(conn=self.conn, limit=10, dry_run=False, check_inbox_first=True)
        self.assertFalse(res.get("aborted"))
        self.assertEqual(res["sent"], 2)

        # Check DB updates for Alpha Tech
        comp1 = db.get_company(self.conn, self.c1_id)
        self.assertEqual(comp1["status"], "Followup-Sent")
        outreaches1 = [o for o in db.list_outreaches(self.conn, self.c1_id) if o["email_type"] == "followup"]
        self.assertEqual(len(outreaches1), 1)
        self.assertEqual(outreaches1[0]["status"], "SUCCESS")
        self.assertEqual(outreaches1[0]["in_reply_to"], "<orig-alpha@alphatech.com>")
        self.assertEqual(outreaches1[0]["references_header"], "<orig-alpha@alphatech.com>")
        self.assertTrue(outreaches1[0]["subject"].startswith("Re: "))

        # Check DB updates for Beta Inc (legacy send with NULL message_id)
        comp2 = db.get_company(self.conn, self.c2_id)
        self.assertEqual(comp2["status"], "Followup-Sent")
        outreaches2 = [o for o in db.list_outreaches(self.conn, self.c2_id) if o["email_type"] == "followup"]
        self.assertEqual(len(outreaches2), 1)
        self.assertEqual(outreaches2[0]["status"], "SUCCESS")
        self.assertIsNone(outreaches2[0]["in_reply_to"])
        self.assertIsNone(outreaches2[0]["references_header"])

        # Delay called between sends (2 candidates -> 1 sleep)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch("check_inbox.run_check", side_effect=RuntimeError("IMAP connection timed out"))
    @patch("followup_pipeline.EmailSender")
    def test_live_run_aborted_when_inbox_check_fails(self, mock_sender_cls, mock_run_check):
        res = run_followups(conn=self.conn, limit=10, dry_run=False, check_inbox_first=True)
        self.assertTrue(res.get("aborted"))
        self.assertEqual(res["sent"], 0)
        self.assertIn("IMAP connection timed out", res.get("error"))
        mock_sender_cls.assert_not_called()

        # Companies remain 'Sent'
        self.assertEqual(db.get_company(self.conn, self.c1_id)["status"], "Sent")
        self.assertEqual(db.get_company(self.conn, self.c2_id)["status"], "Sent")

    @patch("check_inbox.run_check", side_effect=RuntimeError("IMAP connection timed out"))
    def test_dry_run_continues_on_inbox_failure_and_writes_nothing(self, mock_run_check):
        res = run_followups(conn=self.conn, limit=10, dry_run=True, check_inbox_first=True)
        self.assertFalse(res.get("aborted"))
        self.assertEqual(res["candidates"], 2)

        # Nothing changed in DB
        self.assertEqual(db.get_company(self.conn, self.c1_id)["status"], "Sent")
        self.assertEqual(db.get_company(self.conn, self.c2_id)["status"], "Sent")
        followups = [o for o in db.list_outreaches(self.conn) if o["email_type"] == "followup"]
        self.assertEqual(len(followups), 0)


if __name__ == "__main__":
    unittest.main()
