import os
import shutil
import tempfile
import unittest

from cover_letter_generator import CoverLetterGenerator



class TestCoverLetter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.generator = CoverLetterGenerator()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_pdf_without_pitch(self):
        """Generating PDF without pitch uses deterministic content and creates a valid PDF file."""
        pdf_path = os.path.join(self.test_dir, "test_standard.pdf")
        out = self.generator.generate_pdf(
            company_name="Acme Corp",
            role_title="Platform Engineer",
            company_type="fintech",
            recipient_name="Jane Doe",
            company_address="123 Financial Way",
            output_path=pdf_path
        )
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 1000)
        with open(out, "rb") as f:
            header = f.read(5)
            self.assertEqual(header, b"%PDF-")

    def test_generate_pdf_with_pitch_and_escaping(self):
        """Generating PDF with pitch uses pitch lead + bullets and properly escapes & and < >."""
        pdf_path = os.path.join(self.test_dir, "test_pitch.pdf")
        pitch = {
            "lead": "Testing special chars & ampersands in lead <and tags>.",
            "bullets": [
                {
                    "title": "R&D & Scalability",
                    "text": "Tested <xml-like> content & special symbols without breaking ReportLab."
                },
                {
                    "title": "CI/CD & Kubernetes",
                    "text": "Evaluated <tag> formatting & metric: 96% success."
                },
                {
                    "title": "Observability",
                    "text": "Deployed Prometheus & Jaeger dashboards."
                }
            ]
        }
        out = self.generator.generate_pdf(
            company_name="Special & Co <Tech>",
            role_title="Forward Deployed Engineer",
            company_type="ai",
            recipient_name="Recruiting Team",
            company_address="456 Innovation Blvd",
            output_path=pdf_path,
            pitch=pitch
        )
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 1000)
        with open(out, "rb") as f:
            header = f.read(5)
            self.assertEqual(header, b"%PDF-")


if __name__ == "__main__":
    unittest.main()

