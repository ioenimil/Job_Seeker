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
        if words[0].lower() == "nana" and len(words) >= 2:
            return f"Dear Nana {words[1]}"
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


FACT_SHEET = {
    "employer": "AmaliTech Services GmbH",
    "role": "Platform Engineer (DevOps)",
    "education": "Computer Engineering graduate of KNUST (Kwame Nkrumah University of Science and Technology)",
    "certifications": [
        "AWS Certified Solutions Architect – Associate (SAA)",
        "Kubernetes and Cloud Native Associate (KCNA)"
    ],
    "client_projects": [
        "BoaSoft (end-to-end RAG platform)",
        "Turing (agentic tool-calling datasets, exceeded client KPIs for data accuracy and volume, #1 in dataset quality)"
    ]
}

ACHIEVEMENTS = [
    {
        "id": "applied-ai-delivery",
        "title": "Applied AI Delivery",
        "text": "I built an end-to-end RAG system with FastAPI and the Zilliz vector store, grounding answers in a client's verified documents, with a serverless ingestion pipeline and a React frontend for context-aware document interrogation.",
        "tags": ["rag", "fastapi", "zilliz", "react", "applied-ai", "python", "vector-store", "serverless"]
    },
    {
        "id": "evaluation-driven-agents",
        "title": "Evaluation-Driven Agents",
        "text": "I architected a natural-language analytics agent on CopilotKit and Cube Core, and used a DeepEval golden dataset to raise output reliability from 74% to 96% by constraining queries to declared measures and dimensions.",
        "tags": ["ai", "agents", "copilotkit", "cube-core", "deepeval", "evaluation", "llm"]
    },
    {
        "id": "production-platform",
        "title": "Production Platform",
        "text": "I run containerized workloads on production Kubernetes with GitOps delivery via Argo CD, secrets from HashiCorp Vault, and Prometheus, Loki, Grafana, and Jaeger observability, so what I ship stays running.",
        "tags": ["kubernetes", "gitops", "argo-cd", "vault", "prometheus", "loki", "grafana", "jaeger", "observability", "devops"]
    },
    {
        "id": "client-facing-delivery",
        "title": "Client-Facing Delivery",
        "text": "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client's own documents.",
        "tags": ["consultancy", "client-facing", "turing", "boasoft", "rag", "kpi", "benchmarks"]
    },
    {
        "id": "infrastructure-as-code",
        "title": "Infrastructure as Code",
        "text": "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.",
        "tags": ["aws", "terraform", "docker", "vpc", "iac", "cloud"]
    },
    {
        "id": "gitops-secrets",
        "title": "GitOps & Secrets",
        "text": "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.",
        "tags": ["gitops", "argo-cd", "vault", "security", "secrets", "kubernetes"]
    },
    {
        "id": "event-driven-financial-systems",
        "title": "Event-Driven Financial Systems",
        "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging.",
        "tags": ["fintech", "kafka", "knust", "remittance", "event-driven", "hackathon", "acid", "audit"]
    },
    {
        "id": "secure-cicd",
        "title": "Secure CI/CD",
        "text": "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams.",
        "tags": ["ci-cd", "jenkins", "ec2-spot", "keycloak", "sso", "rbac", "security", "aws"]
    },
    {
        "id": "observability-mttr",
        "title": "Observability",
        "text": "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR).",
        "tags": ["observability", "prometheus", "thanos", "loki", "grafana", "jaeger", "mttr", "tracing", "alerting"]
    },
    {
        "id": "aws-infrastructure",
        "title": "AWS Infrastructure",
        "text": "I design scalable AWS environments using Terraform and Docker, including a secure multi-tier VPC and modular application layers.",
        "tags": ["aws", "terraform", "docker", "vpc", "cloud", "iac"]
    },
    {
        "id": "kubernetes-in-production",
        "title": "Kubernetes in Production",
        "text": "I operate containerized workloads on Kubernetes, right-sizing pod requests and limits to eliminate insufficient-capacity scheduling failures and reclaim wasted node capacity.",
        "tags": ["kubernetes", "containers", "resource-optimization", "scheduling", "platform"]
    },
    {
        "id": "systems-monitoring",
        "title": "Systems Monitoring",
        "text": "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with long-term metric retention, distributed tracing, and automated alerting to reduce Mean Time To Resolution (MTTR).",
        "tags": ["observability", "monitoring", "prometheus", "thanos", "loki", "grafana", "jaeger", "mttr", "telecom"]
    },
    {
        "id": "threat-detection-audit",
        "title": "Threat Detection & Audit",
        "text": "I integrated AWS GuardDuty and CloudTrail for automated threat detection and immutable audit trails, enforcing least-privilege governance.",
        "tags": ["security", "aws", "guardduty", "cloudtrail", "audit", "governance", "compliance"]
    },
    {
        "id": "identity-access-control",
        "title": "Identity & Access Control",
        "text": "I secured a Jenkins CI/CD pipeline for 10 developers with Keycloak SSO and role-based access control across 2 sensitive projects and 5 teams.",
        "tags": ["security", "identity", "keycloak", "sso", "rbac", "jenkins", "ci-cd"]
    },
    {
        "id": "infrastructure-velocity",
        "title": "Infrastructure Velocity",
        "text": "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.",
        "tags": ["aws", "terraform", "docker", "vpc", "startup", "velocity"]
    },
    {
        "id": "fast-feedback-loops",
        "title": "Fast Feedback Loops",
        "text": "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.",
        "tags": ["ci-cd", "jenkins", "ec2-spot", "cost-optimization", "developer-velocity"]
    },
    {
        "id": "developer-self-service",
        "title": "Developer Self-Service",
        "text": "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.",
        "tags": ["observability", "prometheus", "loki", "grafana", "jaeger", "self-service", "developer-experience"]
    }
]


def greeting(company_name, recipient_name=None):
    """'Dear Kwame' for a named person, otherwise 'Dear <Company> team'."""
    return salutation(recipient_name) if recipient_name else f"Dear {company_name} team"


def outreach_body(company_name, role, highlights=None, recipient_name=None):
    """Plain-text body of the first cold email. `highlights` are the grounded pitch bullets for this company."""
    if highlights is not None:
        highlights_text = "\n".join(f"- {h}" for h in highlights)
    else:
        highlights_text = (
            "- Provisioning production AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC.\n"
            "- Running GitOps delivery with Argo CD on production Kubernetes, with runtime secrets injected from HashiCorp Vault.\n"
            "- Deploying an observability stack (Prometheus, Thanos, Loki, Grafana, Jaeger) with self-service dashboards for developers.\n"
            "- Building an end-to-end RAG platform (FastAPI, Zilliz, React) grounded in a client's own documents.\n"
            "- Raising an AI analytics agent's reliability from 74% to 96% on a DeepEval evaluation suite."
        )

    return (
        f"{greeting(company_name, recipient_name)},\n\n"
        f"My name is {NAME}. I'm a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering "
        f"graduate of KNUST, with the AWS Certified Solutions Architect – Associate and Kubernetes and Cloud Native "
        f"Associate (KCNA) certifications. Alongside the platform work, I build and ship applied AI systems for clients.\n\n"
        f"I'd like to be considered for {role} work at {company_name}. My CV is attached, along with a cover letter "
        f"written for {company_name}.\n\n"
        f"Some of my work:\n"
        f"{highlights_text}\n\n"
        f"If it's useful, I'd be glad to have a short call with someone on your team or one of your engineering leads.\n\n"
        f"Thanks for reading.\n\n"
        f"Best regards,\n\n"
        + signature()
    )


def followup_body(company_name, role, recipient_name=None):
    """Plain-text body of the follow-up; the original email is quoted below it by followup_pipeline."""
    return (
        f"{greeting(company_name, recipient_name)},\n\n"
        f"A quick follow-up on my earlier note about {role} work at {company_name}.\n\n"
        f"I'm still keen. If there's an opening, or a 10-minute call would be easier than email, I'm happy to work "
        f"around your schedule. The short version of what I'd bring: platform engineering on AWS and Kubernetes, "
        f"GitOps delivery, observability, and applied AI shipped for clients.\n\n"
        f"My CV is attached again so you don't have to dig for it.\n\n"
        f"Best regards,\n\n"
        + signature()
    )

