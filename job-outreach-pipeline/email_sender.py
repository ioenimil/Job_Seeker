import smtplib
import ssl
import os
import email.utils
from email.message import EmailMessage
from config import config
import applicant


class EmailSender:
    def __init__(self, sender_email=None, password=None):
        self.sender_email = sender_email or config.get("SENDER_EMAIL")
        self.password = password or config.get("GMAIL_APP_PASSWORD")
        if not self.sender_email or not self.password:
            raise ValueError("SENDER_EMAIL or GMAIL_APP_PASSWORD is missing in configuration.")

    def _send(self, msg):
        """
        Sets Message-ID, Date, List-Unsubscribe headers BEFORE sending.
        Sends via smtplib.SMTP_SSL("smtp.gmail.com", 465) using smtp.send_message(msg).
        Returns the generated Message-ID.
        """
        domain = self.sender_email.split("@")[-1].rstrip(">") if "@" in self.sender_email else "gmail.com"
        msg_id = email.utils.make_msgid(domain=domain)
        if "Message-ID" in msg:
            del msg["Message-ID"]
        msg["Message-ID"] = msg_id

        if "Date" in msg:
            del msg["Date"]
        msg["Date"] = email.utils.formatdate(localtime=True)

        if "List-Unsubscribe" in msg:
            del msg["List-Unsubscribe"]
        msg["List-Unsubscribe"] = f"<mailto:{self.sender_email}?subject=unsubscribe>"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.sender_email, self.password)
            smtp.send_message(msg)
        return msg_id

    def send_outreach_email(self, recipient_email, company_name, cover_letter_path, cv_path,
                            role_title=applicant.DEFAULT_ROLE, body=None, subject=None):
        """
        Sends an outreach email with the CV and cover letter attached.
        Returns dict: {"ok": bool, "message_id": str|None, "subject": str, "error": str|None}
        """
        subj = subject if subject is not None else applicant.subject(role_title)
        if not recipient_email:
            print("[EmailSender] Error: Recipient email is empty.")
            return {"ok": False, "message_id": None, "subject": subj, "error": "Recipient email is empty."}

        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subj

        email_body = body if body is not None else applicant.outreach_body(company_name, role_title)
        msg.set_content(email_body)

        # Attach Cover Letter
        if cover_letter_path and os.path.exists(cover_letter_path):
            with open(cover_letter_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(cover_letter_path)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            err = f"Cover letter path {cover_letter_path} does not exist."
            print(f"[EmailSender] Error: {err}")
            return {"ok": False, "message_id": None, "subject": subj, "error": err}

        # Attach CV
        if cv_path and os.path.exists(cv_path):
            with open(cv_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(cv_path)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            err = f"CV path {cv_path} does not exist."
            print(f"[EmailSender] Error: {err}")
            return {"ok": False, "message_id": None, "subject": subj, "error": err}

        try:
            print(f"[EmailSender] Connecting to SMTP server to email {recipient_email}...")
            msg_id = self._send(msg)
            print(f"[EmailSender] Successfully sent email to {recipient_email}")
            return {"ok": True, "message_id": msg_id, "subject": subj, "error": None}
        except Exception as e:
            err = str(e)
            print(f"[EmailSender] SMTP Error sending to {recipient_email}: {err}")
            return {"ok": False, "message_id": None, "subject": subj, "error": err}

    def send_followup(self, recipient_email, subject, body, in_reply_to, references, attachments=()):
        """
        Sends a follow-up email.
        Returns dict: {"ok": bool, "message_id": str|None, "subject": str, "error": str|None, "warning": str|None}
        """
        if not recipient_email:
            return {"ok": False, "message_id": None, "subject": subject, "error": "Recipient email is empty."}

        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        warning = None
        if in_reply_to:
            msg["In-Reply-To"] = in_reply_to
            if references:
                msg["References"] = references
        else:
            warning = "in_reply_to is None; sending without threading headers"

        msg.set_content(body)

        # Attachments
        for att_path in (attachments or ()):
            if att_path and os.path.exists(att_path):
                with open(att_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(att_path)
                subtype = "pdf" if file_name.lower().endswith(".pdf") else "octet-stream"
                msg.add_attachment(file_data, maintype="application", subtype=subtype, filename=file_name)
            elif att_path:
                err = f"Attachment path {att_path} does not exist."
                print(f"[EmailSender] Error: {err}")
                res = {"ok": False, "message_id": None, "subject": subject, "error": err}
                if warning:
                    res["warning"] = warning
                return res

        try:
            print(f"[EmailSender] Connecting to SMTP server to email {recipient_email}...")
            msg_id = self._send(msg)
            print(f"[EmailSender] Successfully sent follow-up to {recipient_email}")
            res = {"ok": True, "message_id": msg_id, "subject": subject, "error": None}
            if warning:
                res["warning"] = warning
            return res
        except Exception as e:
            err = str(e)
            print(f"[EmailSender] SMTP Error sending follow-up to {recipient_email}: {err}")
            res = {"ok": False, "message_id": None, "subject": subject, "error": err}
            if warning:
                res["warning"] = warning
            return res
