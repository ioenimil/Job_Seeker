import os
import re
import sqlite3
import tempfile
import unittest

import applicant
import db
import llm_tailor
import style_lint
from cover_letter_generator import CoverLetterGenerator

COMPANY_TYPES = ["ai", "consultancy", "fintech", "isp", "bank", "general_startup"]


def prose(text):
    """Drop the greeting, bullet lines and signature so the rhythm check sees only the paragraphs."""
    body = text.split("Best regards,")[0]
    lines = [l for l in body.splitlines()[1:] if l.strip() and not l.lstrip().startswith("-")
             and not l.rstrip().endswith(":")]
    return " ".join(lines)


class TestStyleLint(unittest.TestCase):
    def test_flags_each_mechanical_pattern(self):
        cases = {
            "We fostered growth across the board.": "stock AI word",
            "Moreover, the platform is stable.": "signpost transition",
            "I shipped the pipeline, highlighting my commitment to quality.": "editorialising ending",
            "It is not just about code; it is about people.": "false antithesis",
            "It is important to note that uptime matters.": "hedge",
            "I hope this email finds you well.": "cliche",
            "Fast—really fast—and cheap—mostly.": "em dashes",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertTrue(any(expected in p for p in style_lint.lint(text)), style_lint.lint(text))

    def test_result_participles_and_source_wording_are_allowed(self):
        # The fact bank states results with participles ("reducing MTTR"); those are facts, not commentary
        self.assertEqual(style_lint.lint("I deployed Loki and Jaeger, reducing Mean Time To Resolution (MTTR)."), [])
        self.assertEqual(style_lint.lint("We harness Kafka.", allowed="we harness kafka for events"), [])

    def test_fact_bank_is_clean(self):
        for fact in applicant.ACHIEVEMENTS:
            with self.subTest(fact=fact["id"]):
                self.assertEqual(style_lint.lint(f"{fact['title']}. {fact['text']}"), [])

    def test_rhythm_flags_flat_cadence_and_repeated_openers(self):
        flat = "I built the thing for them. I deployed the thing for them. I designed the thing for them. I ran it."
        problems = style_lint.rhythm_problems(flat)
        self.assertTrue(any("open with" in p for p in problems))
        uniform = " ".join(["This sentence has exactly twelve words in it, give or take one."] * 4)
        self.assertTrue(any("short sentence" in p for p in style_lint.rhythm_problems(uniform)))


class TestTemplatesStayHuman(unittest.TestCase):
    """The fixed wording goes to every company, so it is held to the same rules as LLM output."""

    def test_cover_letter_variants(self):
        gen = CoverLetterGenerator()
        for ctype in COMPANY_TYPES:
            c = gen.get_letter_content("Acme", applicant.role_for(ctype), ctype)
            paragraphs = " ".join([c["intro"], c["lead"], c["closing"]])
            with self.subTest(company_type=ctype):
                self.assertEqual(style_lint.lint(paragraphs), [])
                self.assertEqual(style_lint.rhythm_problems(c["intro"]), [])

    def test_email_bodies(self):
        bodies = {
            "initial": applicant.outreach_body("Acme", "Platform & DevOps Engineer"),
            "initial-named": applicant.outreach_body("Acme", "Platform & DevOps Engineer", recipient_name="Kwame Mensah"),
            "followup": applicant.followup_body("Acme", "Platform & DevOps Engineer"),
        }
        for name, body in bodies.items():
            with self.subTest(body=name):
                self.assertEqual(style_lint.lint(body), [])
                self.assertEqual(style_lint.rhythm_problems(prose(body)), [])

    def test_greeting_uses_the_contact_name(self):
        self.assertTrue(applicant.outreach_body("Acme", "X", recipient_name="Kwame Mensah").startswith("Dear Kwame,"))
        self.assertTrue(applicant.outreach_body("Acme", "X").startswith("Dear Acme team,"))
        self.assertTrue(applicant.followup_body("Acme", "X", recipient_name="Dr. Ama Owusu").startswith("Dear Dr. Owusu,"))

    def test_credentials_unchanged(self):
        text = applicant.outreach_body("Acme", "X") + CoverLetterGenerator().get_letter_content("Acme", "X", "ai")["intro"]
        for claim in ["AmaliTech Services GmbH", "KNUST", "Solutions Architect", "KCNA", "BoaSoft", "Turing"]:
            self.assertIn(claim, text)


class TestPitchStyleValidation(unittest.TestCase):
    company = {"name": "PepaPay", "website": "https://pepapay.com", "company_type": "fintech",
               "summary": "PepaPay builds mobile payment and merchant collection APIs for businesses in Ghana."}

    def bullet(self, fid, text=None, title=None):
        fact = next(a for a in applicant.ACHIEVEMENTS if a["id"] == fid)
        return {"fact_id": fid, "title": title or fact["title"], "text": text or fact["text"]}

    def pitch(self, n=3, lead="PepaPay builds payment APIs for businesses in Ghana. Here is the work that fits:"):
        ids = ["event-driven-financial-systems", "secure-cicd", "observability-mttr", "gitops-secrets"][:n]
        return {"lead": lead, "bullets": [self.bullet(i) for i in ids]}

    def test_two_or_three_bullets_accepted(self):
        self.assertEqual(llm_tailor.validate_pitch(self.pitch(2), self.company), [])
        self.assertEqual(llm_tailor.validate_pitch(self.pitch(3), self.company), [])

    def test_one_or_four_bullets_rejected(self):
        self.assertTrue(llm_tailor.validate_pitch(self.pitch(1), self.company))
        self.assertTrue(llm_tailor.validate_pitch(self.pitch(4), self.company))

    def test_style_violations_trigger_errors(self):
        bad_lead = self.pitch(lead="Moreover, PepaPay is a pivotal player in payments.")
        errors = llm_tailor.validate_pitch(bad_lead, self.company)
        self.assertTrue(any("Lead style" in e for e in errors), errors)

        bad_bullet = self.pitch()
        bad_bullet["bullets"][1]["text"] += ", showcasing my dedication to security."
        errors = llm_tailor.validate_pitch(bad_bullet, self.company)
        self.assertTrue(any("Bullet 2 style" in e for e in errors), errors)

    def test_fallback_pitch_is_style_clean(self):
        for ctype in COMPANY_TYPES:
            fb = llm_tailor.fallback_pitch({"name": "Acme", "company_type": ctype, "role_title": None})
            with self.subTest(company_type=ctype):
                self.assertEqual(style_lint.lint(fb["lead"]), [])


class TestSchemaV2(unittest.TestCase):
    def test_v1_database_gains_body_column(self):
        path = os.path.join(tempfile.mkdtemp(), "v1.db")
        raw = sqlite3.connect(path)
        raw.execute("CREATE TABLE outreaches (id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL, contact_id INTEGER, "
                    "recipient_email TEXT NOT NULL, email_type TEXT NOT NULL, subject TEXT, message_id TEXT UNIQUE, "
                    "in_reply_to TEXT, references_header TEXT, status TEXT NOT NULL, error TEXT, sent_at TEXT NOT NULL, "
                    "cover_letter_path TEXT)")
        raw.execute("PRAGMA user_version = 1")
        raw.commit()
        raw.close()

        conn = db.connect(path)
        columns = [r["name"] for r in conn.execute("PRAGMA table_info(outreaches)")]
        self.assertIn("body", columns)
        self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 3)
        conn.close()


if __name__ == "__main__":
    unittest.main()
