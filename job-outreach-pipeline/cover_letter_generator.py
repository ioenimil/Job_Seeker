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
            f"I'd like to join {company_name} as a {role_title}. "
            f"I'm a Platform Engineer (DevOps) at AmaliTech Services GmbH and a Computer Engineering graduate of KNUST, "
            f"certified as an AWS Solutions Architect &ndash; Associate and a Kubernetes and Cloud Native Associate (KCNA). "
            f"Platform work is the day job. Next to it I build and ship applied AI against client requirements: most "
            f"recently an end-to-end RAG platform for BoaSoft and agentic tool-calling datasets for Turing. "
            f"I like working where infrastructure, product and the people using it meet."
        )

        achievements_by_id = {ach["id"]: (ach["title"], ach["text"]) for ach in applicant.ACHIEVEMENTS}

        # Paragraph 2 & bullet points based on company type
        if company_type == "ai":
            p2 = (
                "Getting AI out of a demo and into a customer's hands is an engineering problem as much as a "
                "modelling one. I work on both halves:"
            )
            bullets = [
                achievements_by_id["applied-ai-delivery"],
                achievements_by_id["evaluation-driven-agents"],
                achievements_by_id["production-platform"]
            ]

        elif company_type == "consultancy":
            p2 = (
                "Client work rewards engineers who can drop into an unfamiliar setup and work out what the client "
                "actually needs. The harder part is leaving something that still runs after handover. Some of that work:"
            )
            bullets = [
                achievements_by_id["client-facing-delivery"],
                achievements_by_id["infrastructure-as-code"],
                achievements_by_id["gitops-secrets"]
            ]

        elif company_type == "fintech":
            p2 = (
                "Payment systems don't get to be flaky. Every transaction has to be reliable and auditable, and every "
                "release disciplined. Relevant work:"
            )
            bullets = [
                achievements_by_id["event-driven-financial-systems"],
                achievements_by_id["secure-cicd"],
                achievements_by_id["observability-mttr"]
            ]

        elif company_type == "telecom" or company_type == "isp":
            p2 = (
                "A network is only as good as the infrastructure under it and the monitoring watching it. "
                "I build both:"
            )
            bullets = [
                achievements_by_id["aws-infrastructure"],
                achievements_by_id["kubernetes-in-production"],
                achievements_by_id["systems-monitoring"]
            ]

        elif company_type == "bank":
            p2 = (
                "In a bank, security and access control have to live inside the platform, where they can be audited. "
                "That's where I put them:"
            )
            bullets = [
                achievements_by_id["threat-detection-audit"],
                achievements_by_id["identity-access-control"],
                achievements_by_id["gitops-secrets"]
            ]

        else: # startup / general product hunt
            p2 = (
                "Startups need to ship fast without the platform falling over. Automating the slow, error-prone "
                "parts is how I make both possible:"
            )
            bullets = [
                achievements_by_id["infrastructure-velocity"],
                achievements_by_id["fast-feedback-loops"],
                achievements_by_id["developer-self-service"]
            ]

        # Paragraph 3: Closing
        p3 = (
            f"If any of this would help {company_name}, I'd be glad to talk, whether that's a short call or a few "
            f"questions over email. Thanks for reading."
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

    def generate_pdf(self, company_name, role_title, company_type, recipient_name, company_address, output_path, pitch=None):
        """
        Generates a professionally styled PDF cover letter.
        When pitch is provided, uses pitch's lead and bullets.
        """
        import xml.sax.saxutils as saxutils

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

        intro_text = letter["intro"]
        closing_text = letter["closing"]

        if pitch:
            lead_text = saxutils.escape(pitch.get("lead", letter["lead"]))
            raw_bullets = pitch.get("bullets", [])
            # pitch bullets can be list of dicts {"title": ..., "text": ...} or tuples
            normalized_bullets = []
            for b in raw_bullets:
                if isinstance(b, dict):
                    normalized_bullets.append((b.get("title", ""), b.get("text", "")))
                elif isinstance(b, (list, tuple)) and len(b) >= 2:
                    normalized_bullets.append((b[0], b[1]))
        else:
            lead_text = letter["lead"]
            normalized_bullets = letter["bullets"]

        story = []

        story.append(self._letterhead(styles, content_width))
        story.append(HRFlowable(width="100%", thickness=1.2, color=self.accent, spaceBefore=14, spaceAfter=20))
        story.append(self._addressee(styles, content_width, company_name, recipient_name, company_address))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Re: Application for {role_title}", styles["subject"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"{applicant.salutation(recipient_name)},", styles["body"]))

        story.append(Paragraph(intro_text, styles["body"]))
        story.append(Paragraph(lead_text, styles["body"]))
        items = [
            ListItem(Paragraph(f'<font name="{self.semibold}" color="{self.ink.hexval()}">{saxutils.escape(title)}.</font> {saxutils.escape(text)}',
                               styles["bullet"]), spaceAfter=6)
            for title, text in normalized_bullets
        ]
        story.append(ListFlowable(
            items, bulletType="bullet", start="\u2022", bulletFontName=self.semibold, bulletFontSize=10,
            bulletColor=self.accent, leftIndent=16, bulletOffsetY=0,
        ))
        story.append(Spacer(1, 6))
        story.append(Paragraph(closing_text, styles["body"]))

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

