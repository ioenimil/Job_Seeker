import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os

from email_sender import EmailSender
import applicant


class TestEmailSender(unittest.TestCase):
    def setUp(self):
        self.tmp_cv = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        self.tmp_cv.write(b"%PDF-1.4 dummy cv")
        self.tmp_cv.close()

        self.tmp_cl = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        self.tmp_cl.write(b"%PDF-1.4 dummy cover letter")
        self.tmp_cl.close()

    def tearDown(self):
        if os.path.exists(self.tmp_cv.name):
            os.remove(self.tmp_cv.name)
        if os.path.exists(self.tmp_cl.name):
            os.remove(self.tmp_cl.name)

    def test_missing_credentials_raises_value_error(self):
        with patch("config.config.get", return_value=None):
            with self.assertRaises(ValueError):
                EmailSender()

    @patch("smtplib.SMTP_SSL")
    def test_send_outreach_email_sets_and_returns_message_id(self, mock_smtp_ssl):
        smtp_instance = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = smtp_instance

        sender = EmailSender(sender_email="test@example.com", password="password123")
        res = sender.send_outreach_email(
            recipient_email="hr@target.com",
            company_name="Target Corp",
            cover_letter_path=self.tmp_cl.name,
            cv_path=self.tmp_cv.name,
            role_title="Platform Engineer"
        )

        self.assertTrue(res["ok"])
        self.assertIsNotNone(res["message_id"])
        self.assertTrue(res["message_id"].endswith("@example.com>"))
        self.assertEqual(res["subject"], applicant.subject("Platform Engineer"))
        self.assertIsNone(res["error"])

        # Check SMTP calls
        smtp_instance.login.assert_called_once_with("test@example.com", "password123")
        smtp_instance.send_message.assert_called_once()
        sent_msg = smtp_instance.send_message.call_args[0][0]
        self.assertEqual(sent_msg["Message-ID"], res["message_id"])
        self.assertEqual(sent_msg["From"], "test@example.com")
        self.assertEqual(sent_msg["To"], "hr@target.com")
        self.assertEqual(sent_msg["List-Unsubscribe"], "<mailto:test@example.com?subject=unsubscribe>")
        self.assertIsNotNone(sent_msg["Date"])

    @patch("smtplib.SMTP_SSL")
    def test_send_followup_with_threading_headers(self, mock_smtp_ssl):
        smtp_instance = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = smtp_instance

        sender = EmailSender(sender_email="test@example.com", password="password123")
        res = sender.send_followup(
            recipient_email="hr@target.com",
            subject="Re: Platform Engineer Application - Isaac Obo Enimil",
            body="Checking in...",
            in_reply_to="<initial-msg-123@example.com>",
            references="<initial-msg-123@example.com>",
            attachments=(self.tmp_cv.name,)
        )

        self.assertTrue(res["ok"])
        self.assertIsNotNone(res["message_id"])
        self.assertNotIn("warning", res)

        sent_msg = smtp_instance.send_message.call_args[0][0]
        self.assertEqual(sent_msg["In-Reply-To"], "<initial-msg-123@example.com>")
        self.assertEqual(sent_msg["References"], "<initial-msg-123@example.com>")
        self.assertEqual(sent_msg["Subject"], "Re: Platform Engineer Application - Isaac Obo Enimil")

    @patch("smtplib.SMTP_SSL")
    def test_send_followup_legacy_null_id_warning(self, mock_smtp_ssl):
        smtp_instance = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = smtp_instance

        sender = EmailSender(sender_email="test@example.com", password="password123")
        res = sender.send_followup(
            recipient_email="hr@target.com",
            subject="Re: Platform Engineer Application - Isaac Obo Enimil",
            body="Checking in...",
            in_reply_to=None,
            references=None,
            attachments=(self.tmp_cv.name,)
        )

        self.assertTrue(res["ok"])
        self.assertIsNotNone(res["message_id"])
        self.assertIn("warning", res)
        self.assertIn("threading", res["warning"])

        sent_msg = smtp_instance.send_message.call_args[0][0]
        self.assertIsNone(sent_msg.get("In-Reply-To"))
        self.assertIsNone(sent_msg.get("References"))

    @patch("smtplib.SMTP_SSL")
    def test_smtp_error_handling(self, mock_smtp_ssl):
        smtp_instance = MagicMock()
        smtp_instance.send_message.side_effect = Exception("SMTP connection refused")
        mock_smtp_ssl.return_value.__enter__.return_value = smtp_instance

        sender = EmailSender(sender_email="test@example.com", password="password123")
        res = sender.send_followup(
            recipient_email="hr@target.com",
            subject="Re: Followup",
            body="Checking in...",
            in_reply_to=None,
            references=None
        )

        self.assertFalse(res["ok"])
        self.assertIsNone(res["message_id"])
        self.assertIn("SMTP connection refused", res["error"])


if __name__ == "__main__":
    unittest.main()
