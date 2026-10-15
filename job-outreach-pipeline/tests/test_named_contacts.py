"""
Cold outreach goes to named people, not shared inboxes: address classification, the v3 data fix, Exa people
search with Hunter Email Finder, the send gate and the review approval rules.
"""
import os
import shutil
import tempfile
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from rich.console import Console

import db
from contact_enricher import ContactEnricher
from triage import run_review


class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data if json_data is not None else {}
        self.text = str(json_data)

    def json(self):
        return self._json_data


class TempDB(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "named.db")
        self.conn = db.connect(self.db_path)

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.test_dir)


class TestClassifyAddress(unittest.TestCase):
    def test_people_and_shared_inboxes(self):
        cases = {
            "kofi@acme.com": "person",
            "kofi.mensah@acme.com": "person",
            "k_mensah@acme.com": "person",
            "kwame.mensah@gmail.com": "person",
            "careers@acme.com": "departmental",
            "hr.gh@acme.com": "departmental",
            "info@acme.com": "generic",
            "info.gh@acme.com": "generic",
            "hello@acme.com": "generic",
            "data@acme.com": "generic",
            "acmeteam@acme.com": "generic",          # the company's own name
            "acme@gmail.com": "generic",             # company account on free mail
            "teamprogrammers1@gmail.com": "generic", # digits
            "emmaktech@gmail.com": "generic",        # single word on free mail
        }
        for email, kind in cases.items():
            with self.subTest(email=email):
                self.assertEqual(db.classify_address(email, "https://www.acme.com"), kind)

    def test_company_domain_catches_company_named_free_mail(self):
        self.assertEqual(db.classify_address("ammeterlabs@gmail.com", "ammeterlabs.com"), "generic")


class TestSchemaV3(TempDB):
    def test_v2_data_is_reclassified_and_generic_primaries_demoted(self):
        c1, _ = db.upsert_company(self.conn, "Front Desk Co", website="https://frontdesk.com", status="Sent")
        c2, _ = db.upsert_company(self.conn, "Emmak Tech", website="https://emmaktech.com", status="Pending")
        c3, _ = db.upsert_company(self.conn, "Niiosa Labs", website="https://niiosalabs.com", status="Pending")
        k1 = db.add_contact(self.conn, c1, "info@frontdesk.com", source="apify", email_kind="generic", make_primary=True)
        db.add_contact(self.conn, c2, "emmaktech@gmail.com", source="apify", email_kind="person", make_primary=True)
        db.add_contact(self.conn, c3, "michael.ofeor@niiosalabs.com", source="apify", email_kind="person",
                       make_primary=True)
        db.record_send(self.conn, c1, k1, "info@frontdesk.com", email_type="initial", subject="S",
                       message_id="<m1@x>", status="SUCCESS", sent_at="2026-10-01 10:00:00")
        self.conn.execute("PRAGMA user_version = 2")
        self.conn.close()

        self.conn = db.connect(self.db_path)
        self.assertEqual(self.conn.execute("PRAGMA user_version").fetchone()[0], 3)
        self.assertIsNone(db.get_primary_contact(self.conn, c1))
        self.assertEqual(db.list_contacts(self.conn, c2)[0]["email_kind"], "generic")
        self.assertIsNone(db.get_primary_contact(self.conn, c2))
        self.assertEqual(db.get_primary_contact(self.conn, c3)["email_kind"], "person")
        # Follow-ups go to the address the first email went to, whatever the primary is now
        due = db.followup_candidates(self.conn, min_days=6, now="2026-10-10 10:00:00")
        self.assertEqual([d["recipient_email"] for d in due], ["info@frontdesk.com"])


class TestPeopleSearch(TempDB):
    PEOPLE = [
        {"name": "Ama Owusu", "title": "Chief Technology Officer", "profile_url": "https://acme.com/team"},
        {"name": "Kojo Asante", "title": "Talent Director", "profile_url": "https://linkedin.com/in/kojo"},
        {"name": "Efua Mensah", "title": "Head of Sales", "profile_url": "https://acme.com/team"},
    ]

    def enricher(self, hunter_key, session):
        exa = MagicMock()
        exa.find_people.return_value = self.PEOPLE
        return ContactEnricher(self.conn, hunter_key=hunter_key, prospeo_key=None, apify=None, exa=exa,
                               session=session), exa

    def company(self):
        cid, _ = db.upsert_company(self.conn, "Acme", website="https://acme.com", status="Pending")
        return cid, db.get_company(self.conn, cid)

    def test_names_without_hunter_are_kept_for_review(self):
        cid, comp = self.company()
        enricher, exa = self.enricher(None, MagicMock())
        res = enricher.enrich_company(comp)

        exa.find_people.assert_called_once_with("Acme", "acme.com")
        self.assertEqual(res["outcome"], "people_found_no_email")
        people = {p["full_name"]: p for p in db.list_people(self.conn, cid)}
        self.assertEqual(set(people), {"Ama Owusu", "Kojo Asante"})  # sales lead left out
        self.assertIsNone(people["Ama Owusu"]["email"])
        row = db.get_company(self.conn, cid)
        self.assertEqual((row["status"], row["notes"]), ("Pending", "people_found_no_email"))
        self.assertEqual(db.status_counts(self.conn)["people_without_email"], 2)

    def test_hunter_email_finder_fills_in_a_verified_address(self):
        cid, comp = self.company()
        session = MagicMock()

        def fake_get(url, params=None, timeout=None):
            if url.endswith("/domain-search"):
                return MockResponse(200, {"data": {"emails": []}})
            if params["full_name"] == "Ama Owusu":
                return MockResponse(200, {"data": {"email": "ama@acme.com", "score": 92,
                                                   "verification": {"status": "valid"}}})
            return MockResponse(200, {"data": {"email": "kojo@acme.com", "score": 40,
                                               "verification": {"status": "unknown"}}})
        session.get.side_effect = fake_get

        enricher, _ = self.enricher("real_hunter_key", session)
        res = enricher.enrich_company(comp)

        self.assertEqual(res["outcome"], "enriched_person")
        primary = db.get_primary_contact(self.conn, cid)
        self.assertEqual((primary["email"], primary["full_name"], primary["source"]),
                         ("ama@acme.com", "Ama Owusu", "hunter"))
        # The low-score guess for Kojo is not stored
        self.assertIsNone(db.find_contact_by_email(self.conn, "kojo@acme.com"))
        people = {p["full_name"]: p for p in db.list_people(self.conn, cid)}
        self.assertEqual(people["Ama Owusu"]["email"], "ama@acme.com")
        self.assertIsNone(people["Kojo Asante"]["email"])

    def test_people_search_skipped_when_hunter_already_found_a_decision_maker(self):
        cid, comp = self.company()
        session = MagicMock()
        session.get.return_value = MockResponse(200, {"data": {"emails": [
            {"value": "cto@acme.com", "first_name": "Ama", "last_name": "Owusu", "position": "CTO",
             "confidence": 95, "verification": {"status": "valid"}}]}})
        enricher, exa = self.enricher("real_hunter_key", session)
        enricher.enrich_company(comp)
        exa.find_people.assert_not_called()


class TestNoRescrape(TempDB):
    def test_already_scraped_site_is_not_scraped_again_without_refresh(self):
        cid, _ = db.upsert_company(self.conn, "Acme", website="https://acme.com", status="Pending")
        db.add_contact(self.conn, cid, "info@acme.com", source="apify", email_kind="generic")
        apify = MagicMock()
        apify.run_contact_scraper.return_value = []
        enricher = ContactEnricher(self.conn, hunter_key=None, prospeo_key=None, apify=apify, session=MagicMock())

        enricher.run(statuses=("Pending",))
        apify.run_contact_scraper.assert_not_called()
        # The stored info@ still counts, so the company stays Pending rather than "no contact found"
        row = db.get_company(self.conn, cid)
        self.assertEqual((row["status"], row["notes"]), ("Pending", "generic_inbox_only"))

        enricher.run(statuses=("Pending",), refresh=True)
        apify.run_contact_scraper.assert_called_once()


class TestSendGate(TempDB):
    def test_generic_primary_is_never_emailed(self):
        import outreach_pipeline
        cid, _ = db.upsert_company(self.conn, "Front Desk Co", website="https://frontdesk.com", status="Approved")
        kid = db.add_contact(self.conn, cid, "info@frontdesk.com", source="manual", email_kind="generic")
        db.set_primary_contact(self.conn, cid, kid)
        with patch.object(outreach_pipeline, "generate_letter") as gen:
            outreach_pipeline.run_send_emails(self.conn, dry_run=True)
        gen.assert_not_called()
        self.assertEqual(db.list_outreaches(self.conn, cid), [])


class TestRestartSharedInbox(TempDB):
    def sent(self, name, email, kind, status="Sent"):
        cid, _ = db.upsert_company(self.conn, name, website=f"https://{name.lower()}.com", status=status)
        kid = db.add_contact(self.conn, cid, email, source="apify", email_kind=kind)
        db.record_send(self.conn, cid, kid, email, email_type="initial", subject="S", message_id=f"<{name}@x>",
                       status="SUCCESS", sent_at="2026-10-01 10:00:00")
        return cid

    def test_shared_inbox_sends_restart_and_person_sends_do_not(self):
        import outreach_pipeline
        info = self.sent("Infoco", "info@infoco.com", "generic")
        careers = self.sent("Careerco", "careers@careerco.com", "departmental", status="Bounced")
        person = self.sent("Personco", "kofi.mensah@personco.com", "person")
        replied = self.sent("Replyco", "info@replyco.com", "generic", status="Replied")

        outreach_pipeline.restart_shared_inbox_companies(self.conn, dry_run=True)
        self.assertEqual(db.get_company(self.conn, info)["status"], "Sent")

        outreach_pipeline.restart_shared_inbox_companies(self.conn)
        self.assertEqual(db.get_company(self.conn, info)["status"], "Pending")
        self.assertEqual(db.get_company(self.conn, careers)["status"], "Pending")
        self.assertEqual(db.get_company(self.conn, person)["status"], "Sent")
        self.assertEqual(db.get_company(self.conn, replied)["status"], "Replied")
        # No more follow-ups to the shared inboxes; the person still gets theirs
        due = db.followup_candidates(self.conn, min_days=6, now="2026-10-10 10:00:00")
        self.assertEqual([d["company_name"] for d in due], ["Personco"])

    def test_named_person_can_get_a_first_email_after_a_shared_inbox_did(self):
        import outreach_pipeline
        cid = self.sent("Infoco", "info@infoco.com", "generic", status="Approved")
        kid = db.add_contact(self.conn, cid, "ama.owusu@infoco.com", full_name="Ama Owusu", source="hunter",
                             email_kind="person", make_primary=True)
        company, contact = db.get_company(self.conn, cid), db.get_primary_contact(self.conn, cid)
        prior = db.get_initial_outreach(self.conn, cid)
        self.assertFalse(outreach_pipeline.reached_a_person(company, prior, contact))
        # ...but never twice to a person, or to the same address again
        self.assertTrue(outreach_pipeline.reached_a_person(
            company, {"recipient_email": "ama.owusu@infoco.com"}, {"email": "other@infoco.com"}))
        self.assertTrue(outreach_pipeline.reached_a_person(
            company, {"recipient_email": "info@infoco.com"}, {"email": "INFO@infoco.com"}))


@patch("triage.ensure_pitch", return_value={"lead": "", "bullets": [], "grounded": True})
class TestReviewApproval(TempDB):
    def review(self, answers):
        it = iter(answers)
        return run_review(conn=self.conn, statuses=("Pending",), console=Console(file=StringIO()),
                          ask_fn=lambda prompt, choices=None, default=None: next(it))

    def with_primary(self, email, kind):
        cid, _ = db.upsert_company(self.conn, "Acme", website="https://acme.com", status="Pending")
        kid = db.add_contact(self.conn, cid, email, source="manual", email_kind=kind)
        db.set_primary_contact(self.conn, cid, kid)
        return cid

    def test_generic_primary_cannot_be_approved(self, _):
        cid = self.with_primary("info@acme.com", "generic")
        self.review(["A", "S"])
        self.assertEqual(db.get_company(self.conn, cid)["status"], "Skipped")

    def test_departmental_primary_needs_a_yes(self, _):
        cid = self.with_primary("careers@acme.com", "departmental")
        self.review(["A", "n", "N"])
        self.assertEqual(db.get_company(self.conn, cid)["status"], "Pending")
        self.review(["A", "y"])
        self.assertEqual(db.get_company(self.conn, cid)["status"], "Approved")

    def test_add_email_for_a_found_person_then_approve(self, _):
        cid, _ = db.upsert_company(self.conn, "Acme", website="https://acme.com", status="Pending")
        pid = db.add_person(self.conn, cid, "Ama Owusu", title="CTO", profile_url="https://acme.com/team")
        self.review(["E", "4", str(pid), "ama@acme.com", "A"])
        primary = db.get_primary_contact(self.conn, cid)
        self.assertEqual((primary["email"], primary["full_name"], primary["email_kind"]),
                         ("ama@acme.com", "Ama Owusu", "person"))
        self.assertEqual(db.list_people(self.conn, cid)[0]["email"], "ama@acme.com")
        self.assertEqual(db.get_company(self.conn, cid)["status"], "Approved")


if __name__ == "__main__":
    unittest.main()


class TestProspeoParsing(unittest.TestCase):
    """Shapes taken from live Prospeo responses (2026-10-11)."""

    def client(self, responses):
        session = MagicMock()
        session.post.side_effect = responses
        from contact_enricher import ProspeoClient
        return ProspeoClient("key", session=session, min_interval=0, retry_wait=0), session

    def search_item(self, title, email="r****@devarps.com", revealed=False):
        return {"person": {"person_id": "p1", "first_name": "Samuel", "last_name": "Bunnah",
                           "full_name": "Samuel Bunnah", "current_job_title": title,
                           "email": {"status": "VERIFIED", "revealed": revealed, "email": email}}}

    def test_masked_email_is_looked_up_for_a_decision_maker(self):
        enriched = {"error": False, "person": {"email": {"status": "VERIFIED", "revealed": True,
                                                          "email": "richard@devarps.com"}}}
        client, session = self.client([MockResponse(200, {"results": [self.search_item("Founder | CEO")]}),
                                       MockResponse(200, enriched)])
        found = client.find_decision_makers("devarps.com")
        self.assertEqual(found, [{"email": "richard@devarps.com", "full_name": "Samuel Bunnah",
                                  "title": "Founder | CEO", "confidence_score": None,
                                  "verification_status": "valid"}])

    def test_masked_email_of_non_decision_maker_is_dropped_without_a_lookup(self):
        client, session = self.client([MockResponse(200, {"results": [self.search_item("Sales Executive")]})])
        self.assertEqual(client.find_decision_makers("devarps.com"), [])
        self.assertEqual(session.post.call_count, 1)  # no paid lookup

    def test_rate_limit_is_retried_once(self):
        ok = MockResponse(200, {"results": []})
        client, session = self.client([MockResponse(429), ok])
        self.assertEqual(client.find_decision_makers("devarps.com"), [])
        self.assertEqual(session.post.call_count, 2)


class TestMaskedAddressesRejected(TempDB):
    def test_db_refuses_masked_email(self):
        cid, _ = db.upsert_company(self.conn, "Acme", website="https://acme.com")
        with self.assertRaises(ValueError):
            db.add_contact(self.conn, cid, "s*****@acme.com", source="prospeo", email_kind="person")


class TestEnrichmentRobustness(TempDB):
    def test_prospeo_person_with_null_email(self):
        session = MagicMock()
        item = {"person": {"full_name": "No Email", "first_name": None, "last_name": None,
                           "current_job_title": "Sales Lead", "email": {"status": "UNAVAILABLE", "email": None}}}
        session.post.side_effect = [MockResponse(200, {"results": [item]})]
        from contact_enricher import ProspeoClient
        client = ProspeoClient("key", session=session, min_interval=0, retry_wait=0)
        self.assertEqual(client.find_decision_makers("acme.com"), [])

    def test_one_company_error_does_not_lose_the_others(self):
        good, _ = db.upsert_company(self.conn, "Good Co", website="https://good.com", status="Pending")
        bad, _ = db.upsert_company(self.conn, "Bad Co", website="https://bad.com", status="Pending")
        enricher = ContactEnricher(self.conn, hunter_key=None, prospeo_key=None, apify=None, session=MagicMock())
        real = enricher._collect_api_candidates

        def collect(comp, web, dom):
            if comp["name"] == "Bad Co":
                raise TypeError("malformed provider response")
            return [{"email": "kofi.mensah@good.com", "full_name": "Kofi Mensah", "title": "CTO",
                     "source": "hunter", "confidence_score": 95, "verification_status": "valid",
                     "email_kind": "person", "tier": 1, "can_be_primary": True}], ["hunter"]
        enricher._collect_api_candidates = collect

        results = enricher.run(statuses=("Pending",))
        self.assertEqual([r["company_id"] for r in results], [good])
        self.assertEqual(db.get_primary_contact(self.conn, good)["email"], "kofi.mensah@good.com")
        self.assertEqual(db.get_company(self.conn, bad)["status"], "Pending")  # untouched, not Skipped


class TestReadyList(TempDB):
    def test_only_named_decision_makers_are_ready(self):
        import triage
        def company(name, email, full_name, title, kind="person"):
            cid, _ = db.upsert_company(self.conn, name, website=f"https://{name.lower()}.com", status="Pending")
            db.add_contact(self.conn, cid, email, full_name=full_name, title=title, source="hunter",
                           email_kind=kind, make_primary=True)
            return cid
        cto = company("Ctoco", "ama.owusu@ctoco.com", "Ama Owusu", "Chief Technology Officer")
        company("Engco", "kofi@engco.com", "Kofi Boateng", "AI Engineer")             # not a decision-maker
        company("Careerco", "careers@careerco.com", None, None, kind="departmental")  # shared inbox
        company("Nonameco", "toad@nonameco.com", None, "Founder")                      # no name
        self.assertEqual([c["id"] for c, _ in triage.ready_companies(self.conn)], [cto])
