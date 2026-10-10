import os
import csv
import sys
import time
import random
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timedelta
from config import config
import applicant

# Load .env
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

QUEUE_FILE = "outreach_queue.csv"
CV_PATH = applicant.CV_PATH

# Exclusions: add email domains that bounced and company names that already replied
BOUNCED_DOMAINS = []

REPLIED_COMPANIES = []

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def save_queue(queue, fields):
    with open(QUEUE_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(queue)

def get_followup_candidates():
    queue = load_queue()
    candidates = []
    
    # We follow up on emails sent 6 or more days ago
    today = datetime.now()
    threshold_date = today - timedelta(days=6)
    
    for r in queue:
        # Check basic eligibility
        if r["status"] != "Sent" or not r["date_sent"]:
            continue
            
        comp_name_lower = r["company_name"].lower().strip()
        email_lower = r["email"].lower().strip()
        
        # Check active replies exclusion
        if any(rep in comp_name_lower for rep in REPLIED_COMPANIES):
            continue
            
        # Check bounced domains exclusion
        if any(b in email_lower for b in BOUNCED_DOMAINS):
            continue
            
        # Parse date_sent
        date_str = r["date_sent"].split()[0]
        try:
            sent_date = datetime.strptime(date_str, "%Y-%m-%d")
            if sent_date <= threshold_date:
                candidates.append(r)
        except Exception:
            pass
            
    return candidates

def send_followup_email(sender_email, password, r, dry_run=False):
    recipient_email = r["email"]
    company_name = r["company_name"]
    recipient_name = r["recipient_name"]
    company_type = r["company_type"]
    
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    role_title = applicant.role_for(company_type)
    original_subject = applicant.subject(role_title)
    msg["Subject"] = f"Re: {original_subject}"

    body_text = (
        f"{applicant.salutation(recipient_name)},\n\n"
        f"I hope this email finds you well.\n\n"
        f"I am writing to follow up briefly on my application for {role_title} opportunities at {company_name} sent last week.\n\n"
        f"I remain very interested in the work your team is doing, and wanted to check if there are any updates or if you would be open to a brief 10-minute call to connect. "
        f"I would be glad to share how my experience with platform engineering on AWS and Kubernetes, GitOps delivery, observability, and shipping applied AI systems for clients can support your team's goals.\n\n"
        f"I have attached my updated CV for your convenience. Please let me know if there is any other information I can provide.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Best regards,\n\n"
        + applicant.signature()
    )

    # Append original email context to simulate thread reply
    original_date = r["date_sent"]
    body_text += (
        f"\n\n---\n"
        f"Original Message:\n"
        f"From: {sender_email}\n"
        f"Sent: {original_date}\n"
        f"Subject: {original_subject}\n\n"
        + applicant.outreach_body(company_name, role_title)
    )
    
    msg.set_content(body_text)
    
    # Attach CV
    if os.path.exists(CV_PATH):
        with open(CV_PATH, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(CV_PATH)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
    else:
        print(f"Error: CV file not found at {CV_PATH}")
        return False
        
    if dry_run:
        print(f"[DRY-RUN] Would send follow-up to {recipient_email}")
        return True
        
    # Send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Successfully sent follow-up to {recipient_email}")
        return True
    except Exception as e:
        print(f"SMTP Error sending follow-up to {recipient_email}: {e}")
        return False

def run_followups(limit=10, dry_run=False):
    sender_email = config.get("SENDER_EMAIL")
    password = config.get("GMAIL_APP_PASSWORD")
    
    if not sender_email or not password:
        print("Error: Sender email or password missing.")
        sys.exit(1)
        
    candidates = get_followup_candidates()
    print(f"Found {len(candidates)} total candidates for follow-ups.")
    
    if not candidates:
        print("No candidates to follow up with.")
        return
        
    to_send = candidates[:limit]
    print(f"Processing batch of {len(to_send)} follow-ups...")
    
    queue = load_queue()
    fields = []
    if queue:
        fields = list(queue[0].keys())
        # Make sure date_followup_sent is in fields if we want to track it, or we can just update status to "Followup-Sent"
        # Since we cannot change queue schema easily, we will change "status" to "Followup-Sent" and update "date_sent" to reflect followup date
        
    sent_count = 0
    for idx, c in enumerate(to_send):
        comp_name = c["company_name"]
        
        success = send_followup_email(sender_email, password, c, dry_run=dry_run)
        
        if success and not dry_run:
            # Update entry in queue
            for q_row in queue:
                if q_row["company_name"] == comp_name and q_row["email"] == c["email"]:
                    q_row["status"] = "Followup-Sent"
                    q_row["date_sent"] = f"{q_row['date_sent']} | Followup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    break
            save_queue(queue, fields)
            sent_count += 1
            
            # Wait between sends to avoid spam filters
            if idx < len(to_send) - 1:
                delay = random.randint(30, 60)
                print(f"Waiting {delay} seconds...")
                time.sleep(delay)
                
    print(f"Follow-up batch completed. Sent: {sent_count}.")

if __name__ == "__main__":
    # If "run" argument is passed, do live send, otherwise do dry-run
    is_live = len(sys.argv) > 1 and sys.argv[1] == "run"
    run_followups(limit=10, dry_run=not is_live)
