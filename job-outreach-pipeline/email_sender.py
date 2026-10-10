import smtplib
import ssl
import os
from email.message import EmailMessage
from config import config
import applicant

class EmailSender:
    def __init__(self):
        self.sender_email = config.get("SENDER_EMAIL")
        self.password = config.get("GMAIL_APP_PASSWORD")
        if not self.sender_email or not self.password:
            raise ValueError("SENDER_EMAIL or GMAIL_APP_PASSWORD is missing in configuration.")
            
    def send_outreach_email(self, recipient_email, company_name, cover_letter_path, cv_path, role_title=applicant.DEFAULT_ROLE):
        """
        Sends an outreach email with the CV and cover letter attached.
        """
        if not recipient_email:
            print("[EmailSender] Error: Recipient email is empty.")
            return False
            
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = applicant.subject(role_title)

        # Email body (highly professional and brief)
        body = applicant.outreach_body(company_name, role_title)
        msg.set_content(body)
        
        # Attach Cover Letter
        if os.path.exists(cover_letter_path):
            with open(cover_letter_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(cover_letter_path)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            print(f"[EmailSender] Error: Cover letter path {cover_letter_path} does not exist.")
            return False
            
        # Attach CV
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(cv_path)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            print(f"[EmailSender] Error: CV path {cv_path} does not exist.")
            return False
            
        # Send email
        context = ssl.create_default_context()
        try:
            print(f"[EmailSender] Connecting to SMTP server to email {recipient_email}...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(self.sender_email, recipient_email, msg.as_string())
            print(f"[EmailSender] Successfully sent email to {recipient_email}")
            return True
        except Exception as e:
            print(f"[EmailSender] SMTP Error sending to {recipient_email}: {e}")
            return False
