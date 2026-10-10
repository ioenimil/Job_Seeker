import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os
import shutil
import email
from email.message import EmailMessage

import db
from check_inbox import (
    classify_message,
    run_check,
    test_connection,
    backfill_message_ids,
    find_sent_folder,
)


class TestCheckInbox(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_inbox.db")
        self.conn = db.connect(self.db_path)

        # Create sample company & contact
        self.comp_id, _ = db.upsert_company(self.conn, "Acme Corp", website="https://acme.com", status="Sent")
        self.cont_id = db.add_contact(self.conn, self.comp_id, "recruiter@acme.com", full_name="Jane Doe", make_primary=True)

        # Create sample outreach
        self.outreach_id = db.record_send(
            self.conn,
            self.comp_id,
            self.cont_id,
            "recruiter@acme.com",
            email_type="initial",
            subject="Platform Engineer Application - Isaac Obo Enimil",
            message_id="<outreach-acme-1@example.com>",
            status="SUCCESS",
            sent_at="2026-10-07 10:00:00"
        )

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.test_dir)

    def test_classify_dsn_bounce(self):
        raw_msg = (
            "From: MAILER-DAEMON@target.com\n"
            "Subject: Delivery Status Notification (Failure)\n"
            "Content-Type: multipart/report; report-type=delivery-status; boundary=\"bound\"\n"
            "\n"
            "--bound\n"
            "Content-Type: text/plain\n"
            "\n"
            "Delivery to recruiter@acme.com failed.\n"
            "--bound\n"
            "Content-Type: message/delivery-status\n"
            "\n"
            "Final-Recipient: rfc822; recruiter@acme.com\n"
            "Action: failed\n"
            "--bound--\n"
        )
        msg = email.message_from_string(raw_msg)

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "bounce")
        self.assertIn("recruiter@acme.com", details["failed_recipients"])
        self.assertEqual(details["company_id"], self.comp_id)
        self.assertEqual(details["contact_id"], self.cont_id)

    def test_classify_mailer_daemon_plain_bounce(self):
        msg = EmailMessage()
        msg["From"] = "mailer-daemon@googlemail.com"
        msg["Subject"] = "Delivery Status Notification (Failure)"
        msg.set_content("The email account that you tried to reach does not exist: recruiter@acme.com")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "bounce")
        self.assertIn("recruiter@acme.com", details["failed_recipients"])
        self.assertEqual(details["company_id"], self.comp_id)

    def test_classify_x_failed_recipients_bounce(self):
        msg = EmailMessage()
        msg["From"] = "postmaster@corp.com"
        msg["Subject"] = "Undelivered Mail"
        msg["X-Failed-Recipients"] = "recruiter@acme.com"
        msg.set_content("Message could not be delivered.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "bounce")
        self.assertIn("recruiter@acme.com", details["failed_recipients"])

    def test_classify_ooo_auto_reply(self):
        # 1. via Auto-Submitted
        msg1 = EmailMessage()
        msg1["From"] = "recruiter@acme.com"
        msg1["Subject"] = "Re: Platform Engineer Application"
        msg1["Auto-Submitted"] = "auto-replied"
        msg1.set_content("I am out of the office until Monday.")
        kind1, _ = classify_message(msg1, self.conn)
        self.assertEqual(kind1, "auto_reply")

        # 2. via Subject
        msg2 = EmailMessage()
        msg2["From"] = "recruiter@acme.com"
        msg2["Subject"] = "Out of Office: Vacation"
        msg2.set_content("I will respond when I return.")
        kind2, _ = classify_message(msg2, self.conn)
        self.assertEqual(kind2, "auto_reply")

        # 3. via X-Autoreply
        msg3 = EmailMessage()
        msg3["From"] = "recruiter@acme.com"
        msg3["Subject"] = "Re: Application"
        msg3["X-Autoreply"] = "yes"
        msg3.set_content("Auto response.")
        kind3, _ = classify_message(msg3, self.conn)
        self.assertEqual(kind3, "auto_reply")

    def test_classify_human_reply_by_exact_email(self):
        msg = EmailMessage()
        msg["From"] = "Jane Doe <recruiter@acme.com>"
        msg["Subject"] = "Re: Platform Engineer Application - Isaac Obo Enimil"
        msg.set_content("Hi Isaac, thanks for reaching out. We would love to chat with you next week.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "reply")
        self.assertEqual(details["company_id"], self.comp_id)
        self.assertEqual(details["contact_id"], self.cont_id)

    def test_classify_reply_by_company_domain(self):
        # Sender is someone else at Acme Corp not previously known
        msg = EmailMessage()
        msg["From"] = "Engineering Director <cto@acme.com>"
        msg["Subject"] = "Re: Platform Engineer Application"
        msg.set_content("Hi Isaac, Jane forwarded your resume to me. Let's schedule a call.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "reply")
        self.assertEqual(details["company_id"], self.comp_id)

    def test_classify_reply_by_in_reply_to(self):
        # Sender from unknown alias, but threading header matches outreach message_id
        msg = EmailMessage()
        msg["From"] = "talent-ops@partneragency.com"
        msg["Subject"] = "Re: Application"
        msg["In-Reply-To"] = "<outreach-acme-1@example.com>"
        msg.set_content("Hi Isaac, handling Acme's recruiting. Are you free tomorrow?")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "reply")
        self.assertEqual(details["company_id"], self.comp_id)
        self.assertEqual(details["outreach_id"], self.outreach_id)

    def test_classify_unsubscribe(self):
        msg = EmailMessage()
        msg["From"] = "recruiter@acme.com"
        msg["Subject"] = "Re: Application"
        msg.set_content("Please unsubscribe me and remove me from your list.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "unsubscribe")
        self.assertEqual(details["company_id"], self.comp_id)

    def test_classify_unrelated(self):
        msg = EmailMessage()
        msg["From"] = "newsletter@pythonweekly.com"
        msg["Subject"] = "Issue #600"
        msg.set_content("Welcome to this week's issue of Python Weekly with news and articles.")

        kind, _ = classify_message(msg, self.conn)
        self.assertEqual(kind, "unrelated")

    @patch("imaplib.IMAP4_SSL")
    def test_imap_opened_readonly_and_only_peek_fetches_used(self, mock_imap_cls):
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"101"])

        # Prepare test message
        test_msg = EmailMessage()
        test_msg["From"] = "Jane <recruiter@acme.com>"
        test_msg["Subject"] = "Re: Application"
        test_msg["Message-ID"] = "<msg-reply-101@acme.com>"
        test_msg.set_content("Let's talk tomorrow!")
        raw_bytes = test_msg.as_bytes()

        mock_imap.fetch.return_value = ("OK", [(b"101 (BODY[] {123}", raw_bytes)])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            summary = run_check(conn=self.conn, dry_run=False, backfill=False)

        # Verify readonly select
        mock_imap.select.assert_called_with("INBOX", readonly=True)

        # Verify BODY.PEEK[] used
        mock_imap.fetch.assert_called_with(b"101", "(BODY.PEEK[])")

        # Verify company status updated to Replied
        comp = db.get_company(self.conn, self.comp_id)
        self.assertEqual(comp["status"], "Replied")
        self.assertEqual(summary["replies"], 1)
        self.assertEqual(summary["events"], 1)

    @patch("imaplib.IMAP4_SSL")
    def test_idempotent_rerun_reports_zero_new_events(self, mock_imap_cls):
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"101"])

        test_msg = EmailMessage()
        test_msg["From"] = "Jane <recruiter@acme.com>"
        test_msg["Subject"] = "Re: Application"
        test_msg["Message-ID"] = "<idempotent-test-msg@acme.com>"
        test_msg.set_content("Sounds good!")
        raw_bytes = test_msg.as_bytes()
        mock_imap.fetch.return_value = ("OK", [(b"101 (BODY[] {123}", raw_bytes)])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            summary1 = run_check(conn=self.conn, dry_run=False, backfill=False)
            summary2 = run_check(conn=self.conn, dry_run=False, backfill=False)

        self.assertEqual(summary1["events"], 1)
        self.assertEqual(summary2["events"], 0)

    @patch("imaplib.IMAP4_SSL")
    def test_bounce_marks_contact_invalid_and_company_bounced_never_downgrades(self, mock_imap_cls):
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"202"])

        bounce_msg = EmailMessage()
        bounce_msg["From"] = "mailer-daemon@googlemail.com"
        bounce_msg["Subject"] = "Failure"
        bounce_msg["Message-ID"] = "<bounce-msg-1@google.com>"
        bounce_msg.set_content("No such user: recruiter@acme.com")
        raw_bytes = bounce_msg.as_bytes()
        mock_imap.fetch.return_value = ("OK", [(b"202 (BODY[] {123}", raw_bytes)])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            run_check(conn=self.conn, dry_run=False, backfill=False)

        # Contact invalid, company Bounced
        contact = db.find_contact_by_email(self.conn, "recruiter@acme.com")
        self.assertEqual(contact["verification_status"], "invalid")
        comp = db.get_company(self.conn, self.comp_id)
        self.assertEqual(comp["status"], "Bounced")

        # Now test no-downgrade: if company was already 'Replied'
        db.set_company_status(self.conn, self.comp_id, "Replied")
        # Receive another bounce message
        bounce_msg2 = EmailMessage()
        bounce_msg2["From"] = "mailer-daemon@googlemail.com"
        bounce_msg2["Subject"] = "Failure 2"
        bounce_msg2["Message-ID"] = "<bounce-msg-2@google.com>"
        bounce_msg2.set_content("No such user: recruiter@acme.com")
        mock_imap.fetch.return_value = ("OK", [(b"203 (BODY[] {123}", bounce_msg2.as_bytes())])
        mock_imap.search.return_value = ("OK", [b"203"])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            run_check(conn=self.conn, dry_run=False, backfill=False)

        # Company remains 'Replied' (not downgraded to Bounced)
        comp_after = db.get_company(self.conn, self.comp_id)
        self.assertEqual(comp_after["status"], "Replied")

    @patch("imaplib.IMAP4_SSL")
    def test_unsubscribe_sets_replied_and_notes(self, mock_imap_cls):
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"303"])

        unsub_msg = EmailMessage()
        unsub_msg["From"] = "recruiter@acme.com"
        unsub_msg["Subject"] = "Please stop"
        unsub_msg["Message-ID"] = "<unsub-1@acme.com>"
        unsub_msg.set_content("Please remove me from your email list, not interested.")
        raw_bytes = unsub_msg.as_bytes()
        mock_imap.fetch.return_value = ("OK", [(b"303 (BODY[] {123}", raw_bytes)])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            run_check(conn=self.conn, dry_run=False, backfill=False)

        comp = db.get_company(self.conn, self.comp_id)
        self.assertEqual(comp["status"], "Replied")
        self.assertIn("unsubscribe", comp["notes"].lower())

    def test_backfill_matches_by_to_and_subject(self):
        # Create an outreach with NULL message_id
        legacy_outreach_id = db.record_send(
            self.conn,
            self.comp_id,
            self.cont_id,
            "recruiter@acme.com",
            email_type="initial",
            subject="Legacy Application - Isaac Obo Enimil",
            message_id=None,
            status="SUCCESS",
            sent_at="2026-10-07 14:00:00"
        )

        mock_imap = MagicMock()
        mock_imap.list.return_value = ("OK", [b'(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"'])
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"55"])

        header_content = (
            b"Message-ID: <backfilled-id-12345@gmail.com>\r\n"
            b"Subject: Legacy Application - Isaac Obo Enimil\r\n"
            b"\r\n"
        )
        mock_imap.fetch.return_value = ("OK", [(b"55 (BODY[HEADER.FIELDS ...] {50}", header_content)])

        count = backfill_message_ids(self.conn, mock_imap)
        self.assertEqual(count, 1)

        row = self.conn.execute("SELECT message_id FROM outreaches WHERE id = ?", (legacy_outreach_id,)).fetchone()
        self.assertEqual(row["message_id"], "<backfilled-id-12345@gmail.com>")

    @patch("imaplib.IMAP4_SSL")
    def test_test_connection_success(self, mock_imap_cls):
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"42"])

        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            res = test_connection()

        self.assertTrue(res)
        mock_imap.select.assert_called_with("INBOX", readonly=True)
        mock_imap.logout.assert_called_once()


    def test_regression_defect1_newsletter_from_company_domain_is_unrelated(self):
        # Company Acme Corp is in DB. Newsletter from newsletter@acme.com with List-Unsubscribe
        msg = EmailMessage()
        msg["From"] = "newsletter@acme.com"
        msg["Subject"] = "Acme Monthly Tech Digest"
        msg["List-Unsubscribe"] = "<https://acme.com/unsubscribe>"
        msg["Message-ID"] = "<digest-oct-2026@acme.com>"
        msg.set_content("Check out our latest product updates.\nTo stop receiving these, click unsubscribe.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "unrelated")

        # Also test with Precedence: bulk
        msg2 = EmailMessage()
        msg2["From"] = "marketing@acme.com"
        msg2["Subject"] = "Special Promotion"
        msg2["Precedence"] = "bulk"
        msg2["Message-ID"] = "<promo-1@acme.com>"
        msg2.set_content("Special discount inside. Unsubscribe here.")
        kind2, _ = classify_message(msg2, self.conn)
        self.assertEqual(kind2, "unrelated")

    def test_regression_defect1_unassociated_unsubscribe_is_unrelated(self):
        # Random email from stranger asking to unsubscribe with no matching company or outreach
        msg = EmailMessage()
        msg["From"] = "random-person@unknown-domain-xyz.com"
        msg["Subject"] = "Unsubscribe"
        msg["Message-ID"] = "<unsub-stranger@unknown.com>"
        msg.set_content("Please unsubscribe me and remove me from your list.")

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "unrelated")

    def test_regression_defect1_quoted_unsubscribe_in_reply_is_reply(self):
        # Human reply where "unsubscribe" only appears in the quoted original outreach, not in new text
        msg = EmailMessage()
        msg["From"] = "Jane Doe <recruiter@acme.com>"
        msg["Subject"] = "Re: Platform Engineer Application"
        msg["Message-ID"] = "<positive-reply@acme.com>"
        msg.set_content(
            "Hi Isaac,\n\n"
            "We reviewed your profile and would love to schedule a technical interview next Tuesday!\n\n"
            "On Wed, Oct 7, 2026 at 10:00 AM Isaac <ioenimil@gmail.com> wrote:\n"
            "> Dear Recruiting Team,\n"
            "> ...\n"
            "> List-Unsubscribe: <mailto:ioenimil@gmail.com?subject=unsubscribe>\n"
        )

        kind, details = classify_message(msg, self.conn)
        self.assertEqual(kind, "reply")
        self.assertEqual(details["company_id"], self.comp_id)

    @patch("imaplib.IMAP4_SSL")
    def test_regression_defect2_atomic_transaction_rollback(self, mock_imap_cls):
        # Verify that if an error occurs during status update, the inbox event is rolled back atomically
        mock_imap = MagicMock()
        mock_imap_cls.return_value = mock_imap
        mock_imap.select.return_value = ("OK", [b"1"])
        mock_imap.search.return_value = ("OK", [b"999"])

        reply_msg = EmailMessage()
        reply_msg["From"] = "Jane <recruiter@acme.com>"
        reply_msg["Subject"] = "Re: Application"
        reply_msg["Message-ID"] = "<atomic-test-msg@acme.com>"
        reply_msg.set_content("Yes, let's connect!")
        mock_imap.fetch.return_value = ("OK", [(b"999 (BODY[] {123}", reply_msg.as_bytes())])

        # Simulate failure during set_company_status on first run
        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            with patch("db.set_company_status", side_effect=RuntimeError("Simulated DB disk failure")):
                with self.assertRaises(RuntimeError):
                    run_check(conn=self.conn, dry_run=False, backfill=False)

        # The inbox event must NOT exist in the database (rolled back)
        event = self.conn.execute(
            "SELECT * FROM inbox_events WHERE imap_message_id = '<atomic-test-msg@acme.com>'"
        ).fetchone()
        self.assertIsNone(event)
        self.assertEqual(db.get_company(self.conn, self.comp_id)["status"], "Sent")

        # Second run without error: runs cleanly and records both event and status
        with patch("config.config.get", side_effect=lambda k: "val" if k in ("SENDER_EMAIL", "GMAIL_APP_PASSWORD") else None):
            summary = run_check(conn=self.conn, dry_run=False, backfill=False)

        self.assertEqual(summary["events"], 1)
        self.assertEqual(db.get_company(self.conn, self.comp_id)["status"], "Replied")
        event = self.conn.execute(
            "SELECT * FROM inbox_events WHERE imap_message_id = '<atomic-test-msg@acme.com>'"
        ).fetchone()
        self.assertIsNotNone(event)

    def test_regression_defect3_ignore_sender_email(self):
        msg = EmailMessage()
        msg["From"] = "Self Copy <my-outreach@gmail.com>"
        msg["Subject"] = "Test email"
        msg["Message-ID"] = "<self-copy-1@gmail.com>"
        msg.set_content("This is a copy of an email I sent.")

        with patch("config.config.get", return_value="my-outreach@gmail.com"):
            kind, details = classify_message(msg, self.conn)
            self.assertEqual(kind, "unrelated")


if __name__ == "__main__":
    unittest.main()
