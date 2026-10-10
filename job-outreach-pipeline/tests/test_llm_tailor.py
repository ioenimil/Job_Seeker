import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import applicant
import db
from llm_tailor import (
    validate_pitch,
    build_pitch,
    ensure_pitch,
    fallback_pitch
)


class TestLLMTailor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test.db")
        self.conn = db.connect(self.db_path)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.test_dir)

    def test_fact_bank_integrity(self):
        """Fact bank has unique IDs and covers required facts."""
        ids = [ach["id"] for ach in applicant.ACHIEVEMENTS]
        self.assertEqual(len(ids), len(set(ids)), "Achievement IDs must be unique")
        self.assertGreaterEqual(len(ids), 17)

        # Check FACT_SHEET structure
        self.assertIn("employer", applicant.FACT_SHEET)
        self.assertIn("AmaliTech", applicant.FACT_SHEET["employer"])
        self.assertIn("KNUST", applicant.FACT_SHEET["education"])
        self.assertTrue(any("AWS" in c for c in applicant.FACT_SHEET["certifications"]))
        self.assertTrue(any("KCNA" in c for c in applicant.FACT_SHEET["certifications"]))

    def test_outreach_body_with_and_without_highlights(self):
        """outreach_body accepts optional highlights."""
        body_default = applicant.outreach_body("Acme", "DevOps Engineer")
        self.assertIn("Provisioning production AWS infrastructure", body_default)

        custom_highlights = ["Built cool stuff with Python.", "Scaled systems to 1M users."]
        body_custom = applicant.outreach_body("Acme", "DevOps Engineer", highlights=custom_highlights)
        self.assertIn("- Built cool stuff with Python.", body_custom)
        self.assertIn("- Scaled systems to 1M users.", body_custom)
        self.assertNotIn("Provisioning production AWS infrastructure", body_custom)

    def test_validate_pitch_accepts_faithful_rephrase(self):
        """Faithful rephrase of existing achievements passes validation."""
        company = {"name": "Stripe", "summary": "Global payment infrastructure and payment gateway for online commerce."}
        pitch = {
            "lead": "Stripe develops global payment infrastructure and payment gateway systems.",
            "bullets": [
                {
                    "fact_id": "event-driven-financial-systems",
                    "title": "Hackathon Winner",
                    "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming and immutable audit logging."
                },
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD Security",
                    "text": "I engineered a cost-optimized Jenkins pipeline with auto-scaling EC2 Spot agents for 10 developers with Keycloak SSO across 5 cross-functional teams."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Production Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with GitOps delivery via Argo CD, secrets from HashiCorp Vault, and Prometheus, Loki, Grafana, and Jaeger observability."
                }
            ]
        }
        errors = validate_pitch(pitch, company)
        self.assertEqual(errors, [])

    def test_validate_pitch_rejects_invented_metric(self):
        """Rejects bullet with invented metrics or numbers (e.g. 99% or 50 developers)."""
        company = {"name": "Acme", "summary": "Tech startup"}
        pitch = {
            "lead": "Acme builds tech startup solutions.",
            "bullets": [
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD",
                    "text": "I secured a Jenkins setup for 50 developers with Keycloak SSO."
                },
                {
                    "fact_id": "applied-ai-delivery",
                    "title": "AI Delivery",
                    "text": "I built an end-to-end RAG system with FastAPI and the Zilliz vector store."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                }
            ]
        }
        errors = validate_pitch(pitch, company)
        self.assertTrue(any("contains metric/number '50'" in e for e in errors))

    def test_validate_pitch_rejects_invented_technology(self):
        """Rejects bullet with invented technology not in source fact."""
        company = {"name": "Acme", "summary": "Cloud company"}
        pitch = {
            "lead": "Acme is a cloud company.",
            "bullets": [
                {
                    "fact_id": "applied-ai-delivery",
                    "title": "AI Delivery",
                    "text": "I built an end-to-end RAG system with PyTorch, FastAPI and the Zilliz vector store."
                },
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD",
                    "text": "I secured a Jenkins setup for 10 developers with Keycloak SSO across 5 cross-functional teams."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                }
            ]
        }
        errors = validate_pitch(pitch, company)
        self.assertTrue(any("claims technology/token 'pytorch'" in e.lower() for e in errors))

    def test_validate_pitch_rejects_certification_not_in_fact_sheet(self):
        """Rejects certification/degree not in fact sheet."""
        company = {"name": "Acme", "summary": "Cloud company"}
        pitch = {
            "lead": "Acme is a cloud company.",
            "bullets": [
                {
                    "fact_id": "infrastructure-as-code",
                    "title": "AWS",
                    "text": "I design scalable AWS environments with Terraform, as a certified Google Cloud Professional Architect."
                },
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD",
                    "text": "I secured a Jenkins setup for 10 developers with Keycloak SSO across 5 cross-functional teams."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                }
            ]
        }
        errors = validate_pitch(pitch, company)
        self.assertTrue(any("restricted term" in e.lower() or "claims technology/token" in e.lower() for e in errors))

    def test_validate_pitch_rejects_unknown_or_duplicate_fact_ids(self):
        """Rejects unknown fact_id or duplicate fact_ids."""
        company = {"name": "Acme", "summary": "Cloud company"}
        pitch_dup = {
            "lead": "Acme is a cloud company.",
            "bullets": [
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                },
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD",
                    "text": "I secured a Jenkins setup for 10 developers with Keycloak SSO across 5 cross-functional teams."
                }
            ]
        }
        errors_dup = validate_pitch(pitch_dup, company)
        self.assertTrue(any("distinct fact_ids" in e for e in errors_dup))

        pitch_unknown = {
            "lead": "Acme is a cloud company.",
            "bullets": [
                {"fact_id": "non-existent-id", "title": "A", "text": "Something."},
                {"fact_id": "secure-cicd", "title": "B", "text": "I secured a Jenkins setup for 10 developers with Keycloak SSO across 5 cross-functional teams."},
                {"fact_id": "production-platform", "title": "C", "text": "I run containerized workloads on production Kubernetes with Argo CD."}
            ]
        }
        errors_unk = validate_pitch(pitch_unknown, company)
        self.assertTrue(any("unknown fact_id" in e for e in errors_unk))

    def test_validate_pitch_lead_rejects_invented_terms(self):
        """Lead cannot hallucinate high-entropy company terms not in summary."""
        company = {"name": "Acme", "summary": "Online grocery retail and fresh food logistics."}
        pitch = {
            "lead": "Acme specializes in autonomous drone defense cybersecurity operations.",
            "bullets": [
                {
                    "fact_id": "event-driven-financial-systems",
                    "title": "Hackathon",
                    "text": "I won 1st place at the KNUST Technology Week Hackathon with a containerized remittance platform using Kafka for event streaming and immutable audit logging."
                },
                {
                    "fact_id": "secure-cicd",
                    "title": "CI/CD",
                    "text": "I secured a Jenkins setup for 10 developers with Keycloak SSO across 5 cross-functional teams."
                },
                {
                    "fact_id": "production-platform",
                    "title": "Kubernetes",
                    "text": "I run containerized workloads on production Kubernetes with Argo CD."
                }
            ]
        }
        errors = validate_pitch(pitch, company)
        self.assertTrue(any("not found in company summary" in e for e in errors))

    @patch.dict(os.environ, {"LLM_PROVIDER": "none"})
    def test_provider_none_makes_no_network_calls(self):
        """When provider is none, build_pitch returns fallback pitch with no network calls."""
        company_id, _ = db.upsert_company(self.conn, "Acme AI", company_type="ai")
        company = db.get_company(self.conn, company_id)

        with patch("requests.post") as mock_post:
            pitch = build_pitch(company)
            mock_post.assert_not_called()
            self.assertEqual(pitch["provider"], "none")
            self.assertTrue(pitch["grounded"])
            self.assertEqual(len(pitch["bullets"]), 3)

    @patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "test-key", "LLM_MODEL": "claude-sonnet-5-5"})
    def test_retry_then_fallback_path_with_mocked_provider(self):
        """Retry on invalid pitch; if still invalid, falls back gracefully."""
        company_id, _ = db.upsert_company(self.conn, "Acme AI", company_type="ai", summary="AI research lab")
        company = db.get_company(self.conn, company_id)

        bad_response = {
            "content": [
                {
                    "type": "text",
                    "text": '{"lead": "Acme is great.", "bullets": [{"fact_id": "unknown-1", "title": "X", "text": "Fake."}]}'
                }
            ]
        }
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = bad_response

        with patch("requests.post", return_value=mock_resp) as mock_post:
            pitch = build_pitch(company)
            # Should have called LLM twice (initial + 1 retry)
            self.assertEqual(mock_post.call_count, 2)
            self.assertFalse(pitch["grounded"])
            self.assertIsNotNone(pitch["fallback_reason"])
            self.assertEqual(len(pitch["bullets"]), 3)

    @patch.dict(os.environ, {"LLM_PROVIDER": "none"})
    def test_ensure_pitch_caches(self):
        """ensure_pitch writes JSON to companies.pitch and reuses on subsequent calls."""
        company_id, _ = db.upsert_company(self.conn, "Acme AI", company_type="ai")

        # 1st call: generates and caches
        pitch1 = ensure_pitch(self.conn, company_id)
        row1 = db.get_company(self.conn, company_id)
        self.assertIsNotNone(row1["pitch"])

        # 2nd call: returns cached without re-generating
        with patch("llm_tailor.build_pitch") as mock_build:
            pitch2 = ensure_pitch(self.conn, company_id, regenerate=False)
            mock_build.assert_not_called()
            self.assertEqual(pitch1["lead"], pitch2["lead"])

        # 3rd call: regenerate=True forces regeneration
        with patch("llm_tailor.build_pitch", return_value=pitch1) as mock_build:
            ensure_pitch(self.conn, company_id, regenerate=True)
            mock_build.assert_called_once()


if __name__ == "__main__":
    unittest.main()
