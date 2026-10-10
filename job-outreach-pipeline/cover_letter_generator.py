import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
                                Table, TableStyle, ListFlowable, ListItem, KeepTogether)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import applicant

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def register_fonts():
    """
    Registers IBM Plex Sans from fonts/ and returns (regular, medium, semibold, italic) font names.
    Falls back to Helvetica if the font files are missing.
    """
    faces = {
        "Plex": "IBMPlexSans-Regular.ttf",
        "Plex-Medium": "IBMPlexSans-Medium.ttf",
        "Plex-SemiBold": "IBMPlexSans-SemiBold.ttf",
        "Plex-Italic": "IBMPlexSans-Italic.ttf",
    }
    try:
        for name, file_name in faces.items():
            if name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS_DIR, file_name)))
        # So <b> and <i> inside paragraphs map onto the Plex faces
        addMapping("Plex", 0, 0, "Plex")
        addMapping("Plex", 1, 0, "Plex-SemiBold")
        addMapping("Plex", 0, 1, "Plex-Italic")
        addMapping("Plex", 1, 1, "Plex-SemiBold")
        return "Plex", "Plex-Medium", "Plex-SemiBold", "Plex-Italic"
    except Exception as e:
        print(f"[Generator] IBM Plex Sans unavailable ({e}); falling back to Helvetica.")
        return "Helvetica", "Helvetica-Bold", "Helvetica-Bold", "Helvetica-Oblique"


class CoverLetterGenerator:
    def __init__(self):
        self.ink = colors.HexColor("#111827")       # name, headings
        self.body_color = colors.HexColor("#273142") # body text
        self.muted = colors.HexColor("#5B6576")      # contact details, meta
        self.accent = colors.HexColor("#1F4E79")     # deep navy accent
        self.rule = colors.HexColor("#D5DBE3")       # hairlines
        self.regular, self.medium, self.semibold, self.italic = register_fonts()

    def _get_styles(self):
        def S(name, font, size, leading=None, **kw):
            return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading or size * 1.4, **kw)

        return {
            "name": S("Name", self.semibold, 25, 29, textColor=self.ink),
            "headline": S("Headline", self.medium, 10.5, 14, textColor=self.accent, spaceBefore=3),
            "credentials": S("Credentials", self.regular, 8.5, 12, textColor=self.muted, spaceBefore=1),
            "contact": S("Contact", self.regular, 8.5, 13, textColor=self.muted, alignment=TA_RIGHT),
            "meta": S("Meta", self.regular, 9.5, 13.5, textColor=self.muted),
            "meta_strong": S("MetaStrong", self.semibold, 9.5, 13.5, textColor=self.ink),
            "date": S("Date", self.regular, 9.5, 13.5, textColor=self.muted, alignment=TA_RIGHT),
            "subject": S("Subject", self.semibold, 10.5, 14, textColor=self.ink),
            "body": S("Body", self.regular, 10.3, 15.4, textColor=self.body_color, spaceAfter=9),
            "bullet": S("Bullet", self.regular, 10.3, 15.4, textColor=self.body_color),
            "sign": S("Sign", self.regular, 10.3, 15.4, textColor=self.body_color),
            "sign_name": S("SignName", self.semibold, 11.5, 15, textColor=self.ink),
            "sign_title": S("SignTitle", self.regular, 9, 12.5, textColor=self.muted),
            "enclosure": S("Enclosure", self.italic, 8.5, 12, textColor=self.muted),
        }

    def get_letter_content(self, company_name, role_title, company_type):
        """
        Returns the letter text customized by company type: an intro, a lead-in,
        three (title, text) highlights, and a closing paragraph.
        """
        # Paragraph 1: Introduction
        p1 = (
            f"I am writing to express my strong interest in the {role_title} position at {company_name}. "
            f"I am a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, "
            f"certified as an AWS Solutions Architect &ndash; Associate and a Kubernetes and Cloud Native Associate (KCNA). "
            f"Alongside platform work, I build and ship applied AI systems against client requirements, most recently an "
            f"end-to-end RAG platform for BoaSoft and agentic tool-calling datasets for Turing, so I am comfortable working "
            f"where infrastructure, product, and the people using it meet."
        )
        
        # Paragraph 2 & bullet points based on company type
        if company_type == "ai":
            p2 = (
                "Getting AI systems out of a demo and into a customer's hands is as much an engineering problem as a "
                "modelling one. I work across both sides of that gap:"
            )
            b1 = ("Applied AI Delivery", "I built an end-to-end RAG system with FastAPI and the Zilliz vector store, grounding answers in a client's verified documents, with a serverless ingestion pipeline and a React frontend for context-aware document interrogation.")
            b2 = ("Evaluation-Driven Agents", "I architected a natural-language analytics agent on CopilotKit and Cube Core, and used a DeepEval golden dataset to raise output reliability from 74% to 96% by constraining queries to declared measures and dimensions.")
            b3 = ("Production Platform", "I run containerized workloads on production Kubernetes with GitOps delivery via Argo CD, secrets from HashiCorp Vault, and Prometheus, Loki, Grafana, and Jaeger observability, so what I ship stays running.")
            bullets = [b1, b2, b3]

        elif company_type == "consultancy":
            p2 = (
                "Client engagements reward engineers who can land in an unfamiliar environment, understand what the "
                "client actually needs, and leave behind something that keeps running after handover:"
            )
            b1 = ("Client-Facing Delivery", "At Turing I exceeded client KPIs for data accuracy and volume, helping take the team to #1 in dataset quality on client-verified benchmarks; at BoaSoft I shipped a RAG platform built around the client's own documents.")
            b2 = ("Infrastructure as Code", "I design scalable AWS environments with Terraform and Docker, including a secure multi-tier VPC and modular application layers, so environments are reproducible across clients.")
            b3 = ("GitOps &amp; Secrets", "I implement GitOps delivery with Argo CD, treating Git as the single source of truth for cluster state, and inject runtime credentials from HashiCorp Vault to keep secrets out of images and repositories.")
            bullets = [b1, b2, b3]

        elif company_type == "fintech":
            p2 = (
                "Transactional systems demand reliability, auditability, and disciplined delivery. I bring hands-on "
                "experience with each:"
            )
            b1 = ("Event-Driven Financial Systems", "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming, a secure API gateway, an ACID-compliant orchestrator, and immutable audit logging.")
            b2 = ("Secure CI/CD", "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents, and secured a Jenkins setup for 10 developers with Keycloak SSO and RBAC across 5 cross-functional teams.")
            b3 = ("Observability", "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with distributed tracing and automated alerting, reducing Mean Time To Resolution (MTTR).")
            bullets = [b1, b2, b3]

        elif company_type == "telecom" or company_type == "isp":
            p2 = (
                "Telecom and ISP systems rely heavily on robust infrastructure and proactive monitoring. "
                "I bring a strong foundation in both:"
            )
            b1 = ("AWS Infrastructure", "I design scalable AWS environments using Terraform and Docker, including a secure multi-tier VPC and modular application layers.")
            b2 = ("Kubernetes in Production", "I operate containerized workloads on Kubernetes, right-sizing pod requests and limits to eliminate insufficient-capacity scheduling failures and reclaim wasted node capacity.")
            b3 = ("Systems Monitoring", "I deployed Prometheus, Thanos, Loki, Grafana, and Jaeger with long-term metric retention, distributed tracing, and automated alerting to reduce Mean Time To Resolution (MTTR).")
            bullets = [b1, b2, b3]

        elif company_type == "bank":
            p2 = (
                "Financial environments demand strong security posture, auditability, and controlled access. "
                "I bring experience building these into the platform itself:"
            )
            b1 = ("Threat Detection &amp; Audit", "I integrated AWS GuardDuty and CloudTrail for automated threat detection and immutable audit trails, enforcing least-privilege governance.")
            b2 = ("Identity &amp; Access Control", "I secured a Jenkins CI/CD pipeline for 10 developers with Keycloak SSO and role-based access control across 2 sensitive projects and 5 teams.")
            b3 = ("Secrets Management", "I deliver to Kubernetes through Argo CD GitOps and inject runtime credentials from HashiCorp Vault, keeping secrets out of images and repositories.")
            bullets = [b1, b2, b3]

        else: # startup / general product hunt
            p2 = (
                "In fast-growing startups, balancing engineering velocity and system reliability is critical. "
                "I bring automation-first skills that directly support that goal:"
            )
            b1 = ("Infrastructure Velocity", "I provision production-ready AWS infrastructure with Terraform and Docker, including a secure multi-tier VPC and modular application layers.")
            b2 = ("Fast Feedback Loops", "I built a cost-optimized Jenkins CI/CD engine with EC2 Spot agents that auto-scale with build queue depth, speeding up developer feedback while cutting compute cost.")
            b3 = ("Developer Self-Service", "I deployed Prometheus, Loki, Grafana, and Jaeger with self-service dashboards that give developers on-demand insight into their environments and error logs.")
            bullets = [b1, b2, b3]
            

        # Paragraph 3: Closing
        p3 = (
            f"Thank you for your time and consideration. I would welcome the opportunity to discuss how my platform "
            f"engineering and forward-deployed experience can support the technology initiatives at {company_name}."
        )
        return {"intro": p1, "lead": p2, "bullets": bullets, "closing": p3}

    def _draw_page_frame(self, canvas, doc):
        """Navy band across the top edge and a quiet footer."""
        width, height = A4
        canvas.saveState()
        canvas.setFillColor(self.accent)
        canvas.rect(0, height - 6, width, 6, stroke=0, fill=1)
        canvas.setStrokeColor(self.rule)
        canvas.setLineWidth(0.5)
        footer_y = 0.55 * inch
        left, right = doc.leftMargin + 6, width - doc.rightMargin - 6  # match the frame's text edges
        canvas.line(left, footer_y + 10, right, footer_y + 10)
        canvas.setFont(self.regular, 7.5)
        canvas.setFillColor(self.muted)
        canvas.drawString(left, footer_y, f"{applicant.NAME}  \u00b7  Cover Letter")
        canvas.drawRightString(right, footer_y, applicant.WEBSITE_URL.replace("https://", ""))
        canvas.restoreState()

    def _letterhead(self, styles, content_width):
        link = self.accent.hexval()
        left = [
            Paragraph(applicant.NAME, styles["name"]),
            Paragraph(applicant.HEADLINE, styles["headline"]),
            Paragraph(applicant.CREDENTIALS, styles["credentials"]),
        ]
        right = [Paragraph(
            f"{applicant.PHONE}<br/>"
            f'<a href="mailto:{applicant.EMAIL}" color="{link}">{applicant.EMAIL}</a><br/>'
            f'<a href="{applicant.WEBSITE_URL}" color="{link}">ioenimil.me</a><br/>'
            f'<a href="{applicant.LINKEDIN_URL}" color="{link}">linkedin.com/in/isaacoboenimil</a><br/>'
            f'<a href="{applicant.GITHUB_URL}" color="{link}">github.com/ioenimil</a><br/>'
            f"{applicant.LOCATION}",
            styles["contact"]
        )]
        table = Table([[left, right]], colWidths=[content_width * 0.62, content_width * 0.38])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return table

    def _addressee(self, styles, content_width, company_name, recipient_name, company_address):
        lines = [Paragraph(company_name, styles["meta_strong"]), Paragraph(recipient_name, styles["meta"])]
        if company_address:
            lines.append(Paragraph(company_address, styles["meta"]))
        today = datetime.now()
        date_str = f"{today.day} {today.strftime('%B %Y')}"
        table = Table([[lines, Paragraph(date_str, styles["date"])]],
                      colWidths=[content_width * 0.65, content_width * 0.35])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return table

    def generate_pdf(self, company_name, role_title, company_type, recipient_name, company_address, output_path):
        """
        Generates a professionally styled PDF cover letter.
        """
        doc = SimpleDocTemplate(
            output_path, pagesize=A4,
            leftMargin=0.9 * inch, rightMargin=0.9 * inch,
            topMargin=0.75 * inch, bottomMargin=0.95 * inch,
            title=f"Cover Letter - {applicant.NAME} - {company_name}",
            author=applicant.NAME,
            subject=f"{role_title} application",
        )
        # The page frame pads 6pt on each side, so tables must fit doc.width minus that to align with the text
        content_width = doc.width - 12
        styles = self._get_styles()
        letter = self.get_letter_content(company_name, role_title, company_type)
        story = []

        story.append(self._letterhead(styles, content_width))
        story.append(HRFlowable(width="100%", thickness=1.2, color=self.accent, spaceBefore=14, spaceAfter=20))
        story.append(self._addressee(styles, content_width, company_name, recipient_name, company_address))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Re: Application for {role_title}", styles["subject"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"{applicant.salutation(recipient_name)},", styles["body"]))

        story.append(Paragraph(letter["intro"], styles["body"]))
        story.append(Paragraph(letter["lead"], styles["body"]))
        items = [
            ListItem(Paragraph(f'<font name="{self.semibold}" color="{self.ink.hexval()}">{title}.</font> {text}',
                               styles["bullet"]), spaceAfter=6)
            for title, text in letter["bullets"]
        ]
        story.append(ListFlowable(
            items, bulletType="bullet", start="\u2022", bulletFontName=self.semibold, bulletFontSize=10,
            bulletColor=self.accent, leftIndent=16, bulletOffsetY=0,
        ))
        story.append(Spacer(1, 6))
        story.append(Paragraph(letter["closing"], styles["body"]))

        story.append(KeepTogether([
            Spacer(1, 6),
            Paragraph("Sincerely,", styles["sign"]),
            Spacer(1, 18),
            Paragraph(applicant.NAME, styles["sign_name"]),
            Paragraph(applicant.HEADLINE, styles["sign_title"]),
            Spacer(1, 14),
            Paragraph("Enclosure: R\u00e9sum\u00e9", styles["enclosure"]),
        ]))

        doc.build(story, onFirstPage=self._draw_page_frame, onLaterPages=self._draw_page_frame)
        print(f"[Generator] Generated cover letter PDF at: {output_path}")
        return output_path
