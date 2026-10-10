import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import db
from contact_enricher import (
    ContactEnricher,
    classify_title,
    normalize_verification,
    rank_key,
    ProspeoClient,
    main
)


class MockResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data if json_data is not None else {}
        self.text = text or str(json_data)

    def json(self):
        return self._json_data


class TestContactEnricher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_outreach.db")
        self.conn = db.connect(self.db_path)
        self.mock_session = MagicMock()

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_ranking_and_title_classification(self):
        """Title classification correctly maps titles to ranking tiers and tie-breaks."""
        self.assertEqual(classify_title("Chief Technology Officer")[0], 1)
        self.assertEqual(classify_title("CTO & Co-Founder")[0], 1)
        self.assertEqual(classify_title("Vice President of Engineering")[0], 2)
        self.assertEqual(classify_title("Head of Engineering")[0], 2)
        self.assertEqual(classify_title("Engineering Manager")[0], 3)
        self.assertEqual(classify_title("Head of Talent Acquisition")[0], 4)
        self.assertEqual(classify_title("Lead Software Engineer")[0], 5)
        self.assertEqual(classify_title("CEO & Founder")[0], 6)
        self.assertEqual(classify_title("Software Engineer")[0], 7)
        self.assertEqual(classify_title(None)[0], 7)

        # Tie breaking: valid (1) > accept_all (2) > unknown (3), higher confidence is better
        c1 = {"tier": 1, "verification_status": "valid", "confidence_score": 90}
        c2 = {"tier": 1, "verification_status": "valid", "confidence_score": 80}
        c3 = {"tier": 1, "verification_status": "accept_all", "confidence_score": 95}
        c4 = {"tier": 2, "verification_status": "valid", "confidence_score": 99}

        self.assertLess(rank_key(c1), rank_key(c2))  # Higher confidence wins
        self.assertLess(rank_key(c1), rank_key(c3))  # Valid wins over accept_all
        self.assertLess(rank_key(c1), rank_key(c4))  # Tier 1 wins over Tier 2

    def test_hunter_success_with_ranking(self):
        """Hunter domain search succeeds; contacts ranked by title/verification/conf; invalid dropped."""
        comp_id, _ = db.upsert_company(self.conn, "Acme Corp", website="https://acme.com")
        comp = db.get_company(self.conn, comp_id)

        hunter_payload = {
            "data": {
                "emails": [
                    {
                        "value": "vp@acme.com",
                        "first_name": "Bob",
                        "last_name": "Vance",
                        "position": "VP of Engineering",
                        "confidence": 85,
                        "verification": {"status": "valid"}
                    },
                    {
                        "value": "cto@acme.com",
                        "first_name": "Alice",
                        "last_name": "Smith",
                        "position": "Chief Technology Officer",
                        "confidence": 90,
                        "verification": {"status": "valid"}
                    },
                    {
                        "value": "em@acme.com",
                        "first_name": "Charlie",
                        "last_name": "Brown",
                        "position": "Engineering Manager",
                        "confidence": 95,
                        "verification": {"status": "invalid"}  # Invalid: must be dropped
                    },
                    {
                        "value": "founder@acme.com",
                        "first_name": "David",
                        "last_name": "Miller",
                        "position": "Co-founder",
                        "confidence": 75,
                        "verification": {"status": "accept_all"}
                    }
                ]
            }
        }

        self.mock_session.get.return_value = MockResponse(200, hunter_payload)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter_key",
            prospeo_key=None,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "enriched_person")
        self.assertEqual(res["primary_email"], "cto@acme.com")
        self.assertEqual(res["primary_title"], "Chief Technology Officer")
        self.assertEqual(res["contacts_added"], 3)  # cto, vp, founder (em was invalid)

        contacts = db.list_contacts(self.conn, comp_id)
        self.assertEqual(len(contacts), 3)

        # Primary is Alice (CTO)
        primary = db.get_primary_contact(self.conn, comp_id)
        self.assertIsNotNone(primary)
        self.assertEqual(primary["email"], "cto@acme.com")
        self.assertEqual(primary["source"], "hunter")
        self.assertEqual(primary["verification_status"], "valid")
        self.assertEqual(primary["confidence_score"], 90)

    def test_placeholder_keys_skip_provider(self):
        """Placeholder keys (empty or starting with your_) skip provider cleanly without crashing."""
        comp_id, _ = db.upsert_company(self.conn, "Placeholder Co", website="https://place.com")
        comp = db.get_company(self.conn, comp_id)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="your_hunter_key_here",
            prospeo_key="",
            session=self.mock_session
        )

        # Neither Hunter nor Prospeo should make HTTP calls
        res = enricher.enrich_company(comp)

        self.mock_session.get.assert_not_called()
        self.mock_session.post.assert_not_called()
        self.assertEqual(res["outcome"], "no_contact_found")
        self.assertEqual(res["providers_tried"], [])

        updated = db.get_company(self.conn, comp_id)
        self.assertEqual(updated["status"], "Skipped")
        self.assertEqual(updated["notes"], "no_contact_found")

    def test_hunter_429_disables_provider_for_run(self):
        """HTTP 429 stops calling that provider for the rest of the run."""
        id1, _ = db.upsert_company(self.conn, "Company One", website="https://one.com")
        id2, _ = db.upsert_company(self.conn, "Company Two", website="https://two.com")

        # First call returns 429
        self.mock_session.get.return_value = MockResponse(429, text="Rate limit exceeded")

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter_key",
            prospeo_key=None,
            session=self.mock_session
        )

        results = enricher.run(statuses=("Pending",))

        # Hunter should only have been called ONCE for Company One, then disabled for Company Two
        self.assertEqual(self.mock_session.get.call_count, 1)
        self.assertTrue(enricher._hunter_disabled)

    def test_prospeo_used_when_hunter_empty(self):
        """When Hunter yields no contacts, Prospeo is called and enriches decision-makers."""
        comp_id, _ = db.upsert_company(self.conn, "EmptyHunter Inc", website="https://emptyhunter.com")
        comp = db.get_company(self.conn, comp_id)

        # Hunter returns empty emails list
        self.mock_session.get.return_value = MockResponse(200, {"data": {"emails": []}})

        # Prospeo returns Head of Engineering
        prospeo_search_payload = {
            "results": [
                {
                    "person": {
                        "first_name": "Sarah",
                        "last_name": "Connor",
                        "job_title": "Head of Engineering",
                        "email": {
                            "email": "sarah@emptyhunter.com",
                            "status": "VERIFIED"
                        },
                        "confidence_score": 88
                    }
                }
            ]
        }
        self.mock_session.post.return_value = MockResponse(200, prospeo_search_payload)

        mock_apify = MagicMock()
        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            prospeo_key="valid_prospeo",
            apify=mock_apify,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "enriched_person")
        self.assertEqual(res["primary_email"], "sarah@emptyhunter.com")
        self.assertIn("hunter", res["providers_tried"])
        self.assertIn("prospeo", res["providers_tried"])
        mock_apify.run_contact_scraper.assert_not_called()  # Apify not called!

        primary = db.get_primary_contact(self.conn, comp_id)
        self.assertEqual(primary["source"], "prospeo")
        self.assertEqual(primary["verification_status"], "valid")

    def test_apify_fallback_classification(self):
        """Apify fallback: departmental becomes primary, generic stored but not primary, foreign/non-hiring dropped."""
        comp_id, _ = db.upsert_company(self.conn, "ApifyTarget Ltd", website="https://apifytarget.com")
        comp = db.get_company(self.conn, comp_id)

        # Apify returns mixed addresses
        apify_scraped = [
            {
                "url": "https://apifytarget.com",
                "domain": "apifytarget.com",
                "emails": [
                    "recruiting@apifytarget.com",      # Departmental (primary)
                    "info@apifytarget.com",            # Generic (store, not primary)
                    "support@apifytarget.com",         # Non-hiring inbox (drop)
                    "sales@apifytarget.com",           # Non-hiring inbox (drop)
                    "someone@foreigncompany.com",      # Foreign domain (drop)
                    "admin@example.com"                # Placeholder domain (drop)
                ]
            }
        ]

        mock_apify = MagicMock()
        mock_apify.run_contact_scraper.return_value = apify_scraped

        enricher = ContactEnricher(
            self.conn,
            hunter_key=None,
            prospeo_key=None,
            apify=mock_apify,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "enriched_departmental")
        self.assertEqual(res["primary_email"], "recruiting@apifytarget.com")

        contacts = db.list_contacts(self.conn, comp_id)
        emails = {c["email"]: c for c in contacts}

        self.assertIn("recruiting@apifytarget.com", emails)
        self.assertEqual(emails["recruiting@apifytarget.com"]["is_primary"], 1)
        self.assertEqual(emails["recruiting@apifytarget.com"]["email_kind"], "departmental")

        self.assertIn("info@apifytarget.com", emails)
        self.assertEqual(emails["info@apifytarget.com"]["is_primary"], 0)
        self.assertEqual(emails["info@apifytarget.com"]["email_kind"], "generic")

        self.assertNotIn("support@apifytarget.com", emails)
        self.assertNotIn("sales@apifytarget.com", emails)
        self.assertNotIn("someone@foreigncompany.com", emails)
        self.assertNotIn("admin@example.com", emails)

    def test_manual_primary_never_overwritten(self):
        """An existing primary contact whose source is 'manual' is never replaced."""
        comp_id, _ = db.upsert_company(self.conn, "Manual Keep Inc", website="https://manualkeep.com")
        comp = db.get_company(self.conn, comp_id)

        # User manually chose a contact as primary
        manual_id = db.add_contact(
            self.conn,
            comp_id,
            "user_pick@manualkeep.com",
            full_name="User Pick",
            title="Recruiter",
            source="manual",
            make_primary=True
        )

        # Hunter finds a higher-ranking CTO
        hunter_payload = {
            "data": {
                "emails": [
                    {
                        "value": "cto@manualkeep.com",
                        "first_name": "Big",
                        "last_name": "Boss",
                        "position": "CTO",
                        "confidence": 99,
                        "verification": {"status": "valid"}
                    }
                ]
            }
        }
        self.mock_session.get.return_value = MockResponse(200, hunter_payload)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            prospeo_key=None,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "manual_primary_preserved")
        self.assertEqual(res["primary_email"], "user_pick@manualkeep.com")

        # Manual contact is still primary
        primary = db.get_primary_contact(self.conn, comp_id)
        self.assertEqual(primary["id"], manual_id)
        self.assertEqual(primary["source"], "manual")

        # CTO was still added, but not as primary
        cto_contact = db.find_contact_by_email(self.conn, "cto@manualkeep.com")
        self.assertIsNotNone(cto_contact)
        self.assertEqual(cto_contact["is_primary"], 0)

    def test_no_contacts_marks_company_skipped(self):
        """When no usable contacts are found across waterfall, company status is Skipped with note."""
        comp_id, _ = db.upsert_company(self.conn, "Desert Inc", website="https://desert.com")
        comp = db.get_company(self.conn, comp_id)

        # Hunter empty
        self.mock_session.get.return_value = MockResponse(200, {"data": {"emails": []}})
        # Prospeo empty
        self.mock_session.post.return_value = MockResponse(200, {"results": []})
        # Apify empty
        mock_apify = MagicMock()
        mock_apify.run_contact_scraper.return_value = []

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            prospeo_key="valid_prospeo",
            apify=mock_apify,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "no_contact_found")
        self.assertIsNone(res["primary_email"])

        updated = db.get_company(self.conn, comp_id)
        self.assertEqual(updated["status"], "Skipped")
        self.assertEqual(updated["notes"], "no_contact_found")

    def test_generic_only_leaves_pending_with_note(self):
        """When only generic inboxes are found, company remains Pending with notes 'generic_inbox_only'."""
        comp_id, _ = db.upsert_company(self.conn, "Generic Only Ltd", website="https://genericonly.com")
        comp = db.get_company(self.conn, comp_id)

        mock_apify = MagicMock()
        mock_apify.run_contact_scraper.return_value = [
            {
                "url": "https://genericonly.com",
                "domain": "genericonly.com",
                "emails": ["hello@genericonly.com", "info@genericonly.com"]
            }
        ]

        enricher = ContactEnricher(
            self.conn,
            hunter_key=None,
            prospeo_key=None,
            apify=mock_apify,
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "generic_inbox_only")
        self.assertIsNone(res["primary_email"])

        # Status is still Pending, note is generic_inbox_only
        updated = db.get_company(self.conn, comp_id)
        self.assertEqual(updated["status"], "Pending")
        self.assertEqual(updated["notes"], "generic_inbox_only")

        # Contacts were stored with is_primary = 0
        contacts = db.list_contacts(self.conn, comp_id)
        self.assertEqual(len(contacts), 2)
        for c in contacts:
            self.assertEqual(c["is_primary"], 0)
            self.assertEqual(c["email_kind"], "generic")

    def test_dry_run_writes_nothing(self):
        """Dry-run calls providers but rolls back all changes, leaving database untouched."""
        comp_id, _ = db.upsert_company(self.conn, "DryRun Corp", website="https://dryrun.com")

        hunter_payload = {
            "data": {
                "emails": [
                    {
                        "value": "cto@dryrun.com",
                        "first_name": "Dave",
                        "last_name": "Dev",
                        "position": "CTO",
                        "confidence": 95,
                        "verification": {"status": "valid"}
                    }
                ]
            }
        }
        self.mock_session.get.return_value = MockResponse(200, hunter_payload)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            session=self.mock_session
        )

        results = enricher.run(statuses=("Pending",), dry_run=True)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["outcome"], "enriched_person")

        # Database must have NO contacts and company status untouched
        contacts = db.list_contacts(self.conn, comp_id)
        self.assertEqual(len(contacts), 0)

        comp = db.get_company(self.conn, comp_id)
        self.assertEqual(comp["status"], "Pending")

    def test_missing_website_resolved_via_exa(self):
        """Missing website is resolved using Exa search and stored."""
        comp_id, _ = db.upsert_company(self.conn, "NoWebsite Startup")
        comp = db.get_company(self.conn, comp_id)
        self.assertFalse(comp["website"])

        mock_exa = MagicMock()
        mock_exa.search_companies.return_value = [{"url": "https://nowebsite.io/about"}]

        enricher = ContactEnricher(
            self.conn,
            hunter_key=None,
            prospeo_key=None,
            exa=mock_exa,
            session=self.mock_session
        )

        enricher.enrich_company(comp)

        mock_exa.search_companies.assert_called_once_with("NoWebsite Startup official website homepage", num_results=1)
        updated = db.get_company(self.conn, comp_id)
        self.assertEqual(updated["website"], "https://nowebsite.io")
        self.assertEqual(updated["domain"], "nowebsite.io")

    def test_apify_batching_in_run(self):
        """Companies needing Apify fallback are batched into a single Apify call in run()."""
        id1, _ = db.upsert_company(self.conn, "Batch One", website="https://batch1.com")
        id2, _ = db.upsert_company(self.conn, "Batch Two", website="https://batch2.com")

        mock_apify = MagicMock()
        mock_apify.run_contact_scraper.return_value = [
            {
                "url": "https://batch1.com",
                "domain": "batch1.com",
                "emails": ["jobs@batch1.com"]
            },
            {
                "url": "https://batch2.com",
                "domain": "batch2.com",
                "emails": ["careers@batch2.com"]
            }
        ]

        enricher = ContactEnricher(
            self.conn,
            hunter_key=None,
            prospeo_key=None,
            apify=mock_apify,
            session=self.mock_session
        )

        results = enricher.run(statuses=("Pending",))

        self.assertEqual(len(results), 2)
        # Apify should have been called once with both URLs
        mock_apify.run_contact_scraper.assert_called_once()
        urls_passed = mock_apify.run_contact_scraper.call_args[0][0]
        self.assertIn("https://batch1.com", urls_passed)
        self.assertIn("https://batch2.com", urls_passed)

    def test_prospeo_verifies_hunter_best_email(self):
        """Prospeo is used to verify Hunter's best email and updates verification/confidence."""
        comp_id, _ = db.upsert_company(self.conn, "HunterProspeo Co", website="https://hp.com")
        comp = db.get_company(self.conn, comp_id)

        hunter_payload = {
            "data": {
                "emails": [
                    {
                        "value": "cto@hp.com",
                        "first_name": "Carol",
                        "last_name": "Danvers",
                        "position": "CTO",
                        "confidence": 70,
                        "verification": {"status": "accept_all"}
                    }
                ]
            }
        }
        self.mock_session.get.return_value = MockResponse(200, hunter_payload)

        # Prospeo verifies cto@hp.com as VERIFIED with score 98
        prospeo_verify_payload = {
            "response": {
                "email": {
                    "email": "cto@hp.com",
                    "status": "VERIFIED",
                    "score": 98
                }
            }
        }
        self.mock_session.post.return_value = MockResponse(200, prospeo_verify_payload)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            prospeo_key="valid_prospeo",
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "enriched_person")
        self.assertEqual(res["primary_email"], "cto@hp.com")
        self.assertIn("hunter", res["providers_tried"])
        self.assertIn("prospeo", res["providers_tried"])

        primary = db.get_primary_contact(self.conn, comp_id)
        self.assertEqual(primary["verification_status"], "valid")
        self.assertEqual(primary["confidence_score"], 98)

    def test_prospeo_invalidates_hunter_best_email(self):
        """If Prospeo marks Hunter's best email invalid, it is dropped."""
        comp_id, _ = db.upsert_company(self.conn, "DropMe Corp", website="https://dropme.com")
        comp = db.get_company(self.conn, comp_id)

        hunter_payload = {
            "data": {
                "emails": [
                    {
                        "value": "fakecto@dropme.com",
                        "first_name": "Fake",
                        "last_name": "CTO",
                        "position": "CTO",
                        "confidence": 70,
                        "verification": {"status": "unknown"}
                    }
                ]
            }
        }
        self.mock_session.get.return_value = MockResponse(200, hunter_payload)

        prospeo_verify_payload = {
            "response": {
                "email": {
                    "email": "fakecto@dropme.com",
                    "status": "INVALID",
                    "score": 0
                }
            }
        }
        self.mock_session.post.return_value = MockResponse(200, prospeo_verify_payload)

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            prospeo_key="valid_prospeo",
            session=self.mock_session
        )

        res = enricher.enrich_company(comp)

        # fakecto was dropped because Prospeo verified it as INVALID
        self.assertEqual(res["outcome"], "no_contact_found")
        contacts = db.list_contacts(self.conn, comp_id)
        self.assertEqual(len(contacts), 0)

    def test_prospeo_429_disables_prospeo_for_run(self):
        """Prospeo 429 disables Prospeo for the rest of the run."""
        id1, _ = db.upsert_company(self.conn, "Co 1", website="https://co1.com")
        id2, _ = db.upsert_company(self.conn, "Co 2", website="https://co2.com")

        # Prospeo returns 429
        self.mock_session.post.return_value = MockResponse(429, text="Rate limit")

        enricher = ContactEnricher(
            self.conn,
            hunter_key=None,
            prospeo_key="valid_prospeo",
            session=self.mock_session
        )

        enricher.run(statuses=("Pending",))

        self.assertEqual(self.mock_session.post.call_count, 1)
        self.assertTrue(enricher._prospeo_disabled)

    def test_run_skips_existing_person_primary_unless_refresh(self):
        """run() skips companies that already have a person primary unless refresh=True."""
        comp_id, _ = db.upsert_company(self.conn, "Already Done Ltd", website="https://alreadydone.com")
        db.add_contact(
            self.conn,
            comp_id,
            "existing@alreadydone.com",
            full_name="Existing Person",
            title="VP Eng",
            email_kind="person",
            make_primary=True
        )

        enricher = ContactEnricher(
            self.conn,
            hunter_key="valid_hunter",
            session=self.mock_session
        )

        # Run with refresh=False -> skipped!
        res_no_refresh = enricher.run(statuses=("Pending",), refresh=False)
        self.assertEqual(len(res_no_refresh), 0)
        self.assertEqual(enricher.stats["companies_skipped_person_primary"], 1)
        self.mock_session.get.assert_not_called()

        # Run with refresh=True -> processed!
        self.mock_session.get.return_value = MockResponse(200, {"data": {"emails": []}})
        res_refresh = enricher.run(statuses=("Pending",), refresh=True)
        self.assertEqual(len(res_refresh), 1)
        self.mock_session.get.assert_called_once()

    def test_main_cli(self):
        """main() CLI parses arguments, filters by company, and executes run()."""
        comp_id, _ = db.upsert_company(self.conn, "CLI Target", website="https://clitarget.com")

        # Patch db.connect to return self.conn
        with patch("contact_enricher.db.connect", return_value=self.conn):
            # Test company not found
            ret_not_found = main(["--company", "NonExistentCompany"])
            self.assertEqual(ret_not_found, 1)

            # Test company found with dry-run
            ret_ok = main(["--company", "CLI Target", "--dry-run", "--limit", "5"])
            self.assertEqual(ret_ok, 0)


if __name__ == "__main__":
    unittest.main()
