"""
Applicant profile: the single place to edit who the outreach is from.
Content is sourced from https://ioenimil.me and its resume.pdf.
"""

NAME = "Isaac Obo Enimil"
HEADLINE = "Platform (DevOps) &amp; Forward Deployed Engineer"
CREDENTIALS = "AWS Certified Solutions Architect &ndash; Associate&#160;&#160;&middot;&#160;&#160;KCNA"
PHONE = "+233 59 794 4747"
EMAIL = "ioenimil@gmail.com"
LOCATION = "Kumasi, Ghana"
WEBSITE_URL = "https://ioenimil.me"
LINKEDIN_URL = "https://www.linkedin.com/in/isaacoboenimil/"
GITHUB_URL = "https://github.com/ioenimil"

CV_PATH = "Isaac_Obo_Enimil_Resume.pdf"
LETTER_PREFIX = "Isaac_Obo_Enimil_Cover_Letter"

DEFAULT_ROLE = "Platform & DevOps Engineer"
FDE_ROLE = "Forward Deployed Engineer"

# Role pitched per company_type in outreach_queue.csv
ROLE_BY_TYPE = {
    "ai": FDE_ROLE,
    "consultancy": "Forward Deployed / Platform Engineer",
}


def role_for(company_type):
    return ROLE_BY_TYPE.get(company_type, DEFAULT_ROLE)


def letter_filename(company_name):
    safe_name = company_name.replace(" ", "_").replace("/", "_").replace(".", "")
    return f"{LETTER_PREFIX}_{safe_name}.pdf"


GENERIC_RECIPIENT_WORDS = {"team", "manager", "recruiting", "recruitment", "talent", "acquisition", "hr", "resources",
                           "hiring", "services", "solutions", "technology", "tech", "department", "people"}
TITLES = {"mr", "mr.", "ms", "ms.", "mrs", "mrs.", "dr", "dr.", "prof", "prof."}


def salutation(recipient_name):
    """'Dear Recruiting Team' for a team, 'Dear Kwame' or 'Dear Dr. Mensah' for a person."""
    name = recipient_name.strip()
    words = name.split()
    if not words:
        return "Dear Hiring Team"
    if any(w.lower().strip(",.&") in GENERIC_RECIPIENT_WORDS for w in words):
        # "The Recruiting Team" -> "Recruiting Team"
        if words[0].lower() == "the":
            name = " ".join(words[1:])
        return f"Dear {name}"
    if len(words) >= 2:
        if words[0].lower() in TITLES:
            return f"Dear {words[0]} {words[-1]}"
        return f"Dear {words[0]}"
    return f"Dear {name}"


def subject(role):
    return f"{role} Application - {NAME}"


def signature():
    return (
        f"{NAME}\n"
        f"{LOCATION}\n"
        f"Phone: {PHONE}\n"
        f"Portfolio: {WEBSITE_URL}\n"
        f"LinkedIn: {LINKEDIN_URL}\n"
        f"GitHub: {GITHUB_URL}\n"
    )


def outreach_body(company_name, role):
    """Plain-text body of the first cold email (also quoted by follow-ups)."""
    return (
        f"Dear Recruiting Team at {company_name},\n\n"
        f"I hope this email finds you well.\n\n"
        f"My name is {NAME}. I am a Platform Engineer (DevOps) at AmaliTech Services GmbH, a Computer Engineering "
        f"graduate of KNUST, and an AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native "
        f"Associate (KCNA). Alongside platform work, I build and ship applied AI systems against client requirements.\n\n"
        f"I am writing to express my strong interest in {role} opportunities at {company_name}. "
        f"To share details on how my background aligns with your work, I have attached my CV and a tailored cover letter.\n\n"
        f"Some highlights of my work include:\n"
        f"- Provisioning production AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC.\n"
        f"- Running GitOps delivery with Argo CD on production Kubernetes, with runtime secrets injected from HashiCorp Vault.\n"
        f"- Deploying an observability stack (Prometheus, Thanos, Loki, Grafana, Jaeger) with self-service dashboards for developers.\n"
        f"- Building an end-to-end RAG platform (FastAPI, Zilliz, React) grounded in a client's own documents.\n"
        f"- Raising an AI analytics agent's reliability from 74% to 96% on a DeepEval evaluation suite.\n\n"
        f"I would welcome the opportunity to speak briefly with a member of your team or engineering leads about how "
        f"I can add value to {company_name}.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Best regards,\n\n"
        + signature()
    )
