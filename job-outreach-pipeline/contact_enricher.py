"""
Decision-maker enrichment waterfall (Workstream B).

Waterfall per company:
1. Hunter.io Domain Search (type=personal, filter target roles)
2. Prospeo (find decision-makers if Hunter empty, and/or verify Hunter's best email)
3. Apify fallback (batch URLs, classify departmental vs generic, drop non-hiring/foreign)
"""

import os
import sys
import re
import argparse
import urllib.parse
import requests
from config import config
import db
from apify_scraper import ApifyScraper
from exa_search import ExaSearch

# Module constants
HUNTER_BASE_URL = "https://api.hunter.io/v2"
HUNTER_DOMAIN_SEARCH_PATH = "/domain-search"

PROSPEO_BASE_URL = "https://api.prospeo.io"
PROSPEO_SEARCH_PERSON_PATH = "/search-person"
PROSPEO_ENRICH_PERSON_PATH = "/enrich-person"

NON_HIRING_INBOXES = [
    "support", "sales", "privacy", "press", "media", "legal", "noreply", "no-reply",
    "billing", "abuse", "security", "dpo", "compliance", "complaints", "fraud",
    "help", "investor", "training", "comms", "sellers", "marketing", "autoed"
]

PLACEHOLDER_EMAIL_DOMAINS = [
    "yourcompany.com", "example.com", "domain.com", "email.com", "company.com",
    "youremail.com", "yourdomain.com"
]

DEPARTMENTAL_INBOXES = {
    "recruiting", "recruitment", "careers", "jobs", "hr", "talent", "people",
    "hiring", "tech", "engineering", "dev"
}

GENERIC_INBOXES = {
    "info", "hello", "contact", "office", "admin", "enquiries", "inquiries",
    "mail", "team"
}


def is_configured(key):
    """Returns True if the API key is present and not a placeholder."""
    if not key or not isinstance(key, str):
        return False
    k = key.strip()
    if not k or k.startswith("your_"):
        return False
    return True


def normalize_verification(status):
    """
    Normalises provider verification values onto db.VERIFICATION:
    ('valid', 'invalid', 'accept_all', 'unknown').
    """
    if not status or not isinstance(status, str):
        return "unknown"
    s = status.strip().lower()
    if s in ("valid", "verified", "deliverable"):
        return "valid"
    if s in ("invalid", "undeliverable", "unverified"):
        return "invalid"
    if s in ("accept_all", "accept-all", "catch_all", "catch-all", "risky"):
        return "accept_all"
    return "unknown"


def classify_title(title):
    """
    Classify person title into ranking tiers (lower number = better):
    1. CTO / Chief Technology Officer
    2. VP/Head/Director of Engineering
    3. Engineering Manager
    4. Head of Talent / Talent Acquisition / Recruiting lead
    5. Technical Lead / Tech Lead / Lead Engineer
    6. Founder / Co-founder / CEO
    7. other person contacts
    """
    if not title:
        return 7, "Other Person"
    t = title.lower().strip()
    
    # Tier 1: CTO / Chief Technology Officer
    if re.search(r"\bcto\b", t) or re.search(r"chief\s+technol(ogy|ical)\s+officer", t) or "chief technical officer" in t:
        return 1, "CTO"
        
    # Tier 2: VP/Head/Director of Engineering
    if (re.search(r"\b(vp|vice\s+president)\b.*(engineer|tech)", t) or
        re.search(r"head\s+of\s+(engineering|tech|technology|software)", t) or
        re.search(r"director\s+of\s+(engineering|tech|technology|software)", t) or
        re.search(r"(engineering|technical)\s+director", t)):
        return 2, "VP/Head/Director of Engineering"
        
    # Tier 3: Engineering Manager
    if re.search(r"(software\s+)?(engineering|eng)\s+manager", t):
        return 3, "Engineering Manager"
        
    # Tier 4: Head of Talent / Talent Acquisition / Recruiting lead
    if (re.search(r"head\s+of\s+talent", t) or
        re.search(r"head\s+of\s+recruit", t) or
        re.search(r"talent\s+acquisition\s+(lead|head|director|manager)", t) or
        re.search(r"(lead|head|director)\s+of\s+talent\s+acquisition", t) or
        re.search(r"\btalent\s+acquisition\b", t) or
        re.search(r"recruit(ing|ment)\s+lead", t) or
        re.search(r"lead\s+recruiter", t)):
        return 4, "Head of Talent / Recruiting Lead"
        
    # Tier 5: Technical Lead / Tech Lead / Lead Engineer
    if (re.search(r"\btech(nical)?\s+lead\b", t) or
        re.search(r"lead\s+(software\s+)?(engineer|developer|architect)", t) or
        re.search(r"principal\s+(software\s+)?(engineer|developer)", t)):
        return 5, "Technical Lead / Lead Engineer"
        
    # Tier 6: Founder / Co-founder / CEO
    if (re.search(r"\bco-?founder\b", t) or
        re.search(r"\bfounder\b", t) or
        re.search(r"\bceo\b", t) or
        re.search(r"chief\s+executive\s+officer", t)):
        return 6, "Founder / CEO"
        
    return 7, "Other Person"


def rank_key(contact):
    """
    Sort key for candidate ranking (lower = better):
    Tie-break on verification ('valid' > 'accept_all' > 'unknown'/None; drop 'invalid') then confidence.
    """
    verif_order = {"valid": 1, "accept_all": 2, "unknown": 3}
    v_score = verif_order.get(contact.get("verification_status"), 3)
    conf = contact.get("confidence_score")
    conf_score = -int(conf) if conf is not None else 0
    return (contact.get("tier", 7), v_score, conf_score)


class ProspeoClient:
    """
    Prospeo API adapter class.
    Endpoints and base URL are module constants. Authenticates via X-KEY header.
    """
    def __init__(self, api_key=None, session=None, base_url=PROSPEO_BASE_URL, timeout=15):
        self.api_key = api_key
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self):
        return {
            "X-KEY": self.api_key or "",
            "Content-Type": "application/json",
            "User-Agent": "JobOutreachPipeline/1.0"
        }

    def find_decision_makers(self, domain):
        """
        Searches for decision-maker person contacts for the domain.
        Returns list of dicts: [{'email', 'full_name', 'title', 'confidence_score', 'verification_status'}].
        On quota / auth error, returns {'error_status': code}.
        """
        if not domain:
            return []
        url = f"{self.base_url}{PROSPEO_SEARCH_PERSON_PATH}"
        payload = {
            "page": 1,
            "filters": {
                "company": {
                    "websites": {
                        "include": [domain]
                    }
                }
            }
        }
        res = self.session.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return []

        data = res.json()
        contacts = []
        
        # Handle various response formats (official 'results' list, 'data' list, or 'response' list)
        items = data.get("results") or data.get("data") or data.get("response") or data.get("emails") or []
        if isinstance(items, list):
            for item in items:
                # Official person schema is nested under 'person'
                p = item.get("person", item) if isinstance(item, dict) else {}
                if not isinstance(p, dict):
                    continue
                
                # Check email field (might be nested dict, or string)
                em_field = p.get("email") or p.get("work_email") or ""
                em_str = ""
                verif_status = "unknown"
                if isinstance(em_field, dict):
                    em_str = em_field.get("email", "")
                    verif_status = em_field.get("status", "unknown")
                elif isinstance(em_field, str):
                    em_str = em_field
                    verif_status = p.get("verification_status") or p.get("status") or "unknown"
                    
                first = p.get("first_name", "")
                last = p.get("last_name", "")
                full_name = p.get("full_name") or f"{first} {last}".strip() or None
                title = p.get("job_title") or p.get("title") or p.get("position")
                conf = p.get("confidence_score") or p.get("score") or p.get("confidence")

                # If no email revealed in search, attempt enrichment if person_id or name exists
                person_id = p.get("person_id") or p.get("id")
                if not em_str and (person_id or (first and last)):
                    try:
                        enrich_res = self.enrich_person(person_id=person_id, first_name=first, last_name=last, domain=domain)
                        if isinstance(enrich_res, dict) and "email" in enrich_res:
                            em_str = enrich_res["email"]
                            verif_status = enrich_res.get("verification_status", verif_status)
                            conf = enrich_res.get("confidence_score", conf)
                    except Exception:
                        pass

                if em_str and "@" in em_str:
                    contacts.append({
                        "email": em_str.strip().lower(),
                        "full_name": full_name,
                        "title": title,
                        "confidence_score": conf,
                        "verification_status": normalize_verification(verif_status)
                    })
        return contacts

    def enrich_person(self, person_id=None, first_name=None, last_name=None, domain=None):
        """Enriches a specific person record."""
        url = f"{self.base_url}{PROSPEO_ENRICH_PERSON_PATH}"
        data_payload = {}
        if person_id:
            data_payload["person_id"] = person_id
        if first_name:
            data_payload["first_name"] = first_name
        if last_name:
            data_payload["last_name"] = last_name
        if domain:
            data_payload["company_website"] = domain
            
        res = self.session.post(url, json={"data": data_payload}, headers=self._headers(), timeout=self.timeout)
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return {}
            
        data = res.json()
        resp_obj = data.get("response") or data.get("data") or data
        em_obj = resp_obj.get("email") or {}
        if isinstance(em_obj, dict):
            return {
                "email": em_obj.get("email"),
                "verification_status": normalize_verification(em_obj.get("status")),
                "confidence_score": em_obj.get("score")
            }
        elif isinstance(em_obj, str):
            return {
                "email": em_obj,
                "verification_status": normalize_verification(resp_obj.get("status")),
                "confidence_score": resp_obj.get("score")
            }
        return {}

    def verify_email(self, email):
        """
        Verifies an email using Prospeo /enrich-person with email parameter.
        Returns dict with 'status' (normalised verification) and optional 'confidence_score'.
        """
        url = f"{self.base_url}{PROSPEO_ENRICH_PERSON_PATH}"
        res = self.session.post(url, json={"data": {"email": email}}, headers=self._headers(), timeout=self.timeout)
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return {}
        data = res.json()
        resp_obj = data.get("response") or data.get("data") or data
        em_obj = resp_obj.get("email") or {}
        if isinstance(em_obj, dict):
            return {
                "status": normalize_verification(em_obj.get("status")),
                "confidence_score": em_obj.get("score")
            }
        elif isinstance(em_obj, str):
            return {
                "status": normalize_verification(resp_obj.get("status")),
                "confidence_score": resp_obj.get("score")
            }
        return {}


class ContactEnricher:
    """
    Decision-maker enrichment waterfall per company.
    """
    def __init__(self, conn, hunter_key=None, prospeo_key=None, apify=None, exa=None, session=None):
        self.conn = conn
        self.hunter_key = hunter_key if hunter_key is not None else config.get("HUNTER_API_KEY")
        self.prospeo_key = prospeo_key if prospeo_key is not None else config.get("PROSPEO_API_KEY")
        self._apify = apify
        self._exa = exa
        self.session = session or requests.Session()
        
        self._hunter_disabled = False
        self._prospeo_disabled = False
        self._apify_disabled = False
        self._exa_disabled = False

        self.stats = {
            "companies_evaluated": 0,
            "companies_processed": 0,
            "companies_skipped_person_primary": 0,
            "outcomes": {
                "enriched_person": 0,
                "enriched_departmental": 0,
                "generic_inbox_only": 0,
                "no_contact_found": 0,
                "manual_primary_preserved": 0,
            },
            "provider_calls": {
                "hunter": 0,
                "prospeo": 0,
                "apify": 0,
                "exa": 0,
            },
            "contacts_added": 0,
        }

    @property
    def apify(self):
        if self._apify is None and not self._apify_disabled:
            token = config.get("APIFY_API_TOKEN")
            if not is_configured(token):
                self._apify_disabled = True
                print("[Enrich] Apify API token not configured or placeholder; skipping.")
                return None
            try:
                self._apify = ApifyScraper(token=token, session=self.session)
            except Exception as e:
                self._apify_disabled = True
                print(f"[Enrich] Could not initialize ApifyScraper: {e}")
                return None
        return self._apify

    @property
    def exa(self):
        if self._exa is None and not self._exa_disabled:
            key = config.get("EXA_API_KEY")
            if not is_configured(key):
                self._exa_disabled = True
                print("[Enrich] Exa API key not configured or placeholder; skipping.")
                return None
            try:
                self._exa = ExaSearch()
            except Exception as e:
                self._exa_disabled = True
                print(f"[Enrich] Could not initialize ExaSearch: {e}")
                return None
        return self._exa

    def _resolve_missing_website(self, company_id, company_name):
        """Uses ExaSearch to find company website if missing."""
        if not self.exa or self._exa_disabled:
            return "", ""
        print(f"[Enrich] Website missing for '{company_name}'. Searching via Exa...")
        self.stats["provider_calls"]["exa"] += 1
        try:
            results = self.exa.search_companies(f"{company_name} official website homepage", num_results=1)
            if results and results[0].get("url"):
                parsed = urllib.parse.urlparse(results[0]["url"])
                web = f"{parsed.scheme}://{parsed.netloc}".lower()
                dom = db.bare_domain(web)
                db.update_company(self.conn, company_id, website=web, domain=dom)
                print(f"[Enrich] Resolved website for '{company_name}': {web}")
                return web, dom
        except Exception as e:
            print(f"[Enrich] Exa search failed for '{company_name}': {e}")
        return "", ""

    def enrich_company(self, company_row, apify_items=None) -> dict:
        """
        Executes waterfall for a single company row (Row or dict).
        Returns:
            {"company_id", "contacts_added", "primary_email", "primary_title", "providers_tried", "outcome"}
        """
        company_id = company_row["id"]
        company_name = company_row["name"]
        website = company_row["website"] or ""
        domain = company_row["domain"] or ""

        # Missing website resolution via Exa
        if not website:
            website, domain = self._resolve_missing_website(company_id, company_name)
        elif not domain:
            domain = db.bare_domain(website)
            db.update_company(self.conn, company_id, domain=domain)

        providers_tried = []
        candidates = []

        # =========================================================================
        # 1. Hunter.io Domain Search
        # =========================================================================
        if not is_configured(self.hunter_key):
            print("[Enrich] Hunter API key not configured or placeholder; skipping.")
        elif self._hunter_disabled:
            print("[Enrich] Hunter provider disabled for this run; skipping.")
        elif domain:
            providers_tried.append("hunter")
            self.stats["provider_calls"]["hunter"] += 1
            url = f"{HUNTER_BASE_URL}{HUNTER_DOMAIN_SEARCH_PATH}"
            params = {
                "domain": domain,
                "api_key": self.hunter_key,
                "type": "personal"
            }
            try:
                res = self.session.get(url, params=params, timeout=15)
                if res.status_code in (401, 402, 429):
                    self._hunter_disabled = True
                    print(f"[Enrich] Hunter returned HTTP {res.status_code}; disabling provider for remainder of run.")
                elif res.status_code == 200:
                    data = res.json()
                    emails_data = data.get("data", {}).get("emails", [])
                    for em in emails_data:
                        val = em.get("value")
                        if not val or "@" not in val:
                            continue
                        verif = em.get("verification")
                        v_status = verif.get("status") if isinstance(verif, dict) else verif
                        norm_v = normalize_verification(v_status)
                        if norm_v == "invalid":
                            continue  # Drop invalid verification

                        pos = em.get("position")
                        tier, norm_role = classify_title(pos)
                        first_name = em.get("first_name") or ""
                        last_name = em.get("last_name") or ""
                        full_name = f"{first_name} {last_name}".strip() or em.get("full_name") or None

                        # Keep people whose position matches target roles
                        if tier <= 7:
                            candidates.append({
                                "email": val.strip().lower(),
                                "full_name": full_name,
                                "title": pos or norm_role,
                                "source": "hunter",
                                "confidence_score": em.get("confidence"),
                                "verification_status": norm_v,
                                "email_kind": "person",
                                "tier": tier,
                            })
                else:
                    print(f"[Enrich] Hunter returned HTTP {res.status_code}: {res.text}")
            except requests.RequestException as e:
                print(f"[Enrich] Hunter request exception: {e}")

        # =========================================================================
        # 2. Prospeo
        # =========================================================================
        if not is_configured(self.prospeo_key):
            print("[Enrich] Prospeo API key not configured or placeholder; skipping.")
        elif self._prospeo_disabled:
            print("[Enrich] Prospeo provider disabled for this run; skipping.")
        else:
            prospeo_client = ProspeoClient(self.prospeo_key, session=self.session)
            if candidates:
                # (b) Verify Hunter's best email
                best_hunter = min(candidates, key=rank_key)
                providers_tried.append("prospeo")
                self.stats["provider_calls"]["prospeo"] += 1
                try:
                    verif_data = prospeo_client.verify_email(best_hunter["email"])
                    if verif_data.get("error_status") in (401, 402, 429):
                        self._prospeo_disabled = True
                        print(f"[Enrich] Prospeo returned HTTP {verif_data['error_status']}; disabling provider for remainder of run.")
                    elif "status" in verif_data:
                        pv_status = verif_data["status"]
                        if pv_status == "invalid":
                            candidates.remove(best_hunter)
                        else:
                            best_hunter["verification_status"] = pv_status
                            if verif_data.get("confidence_score") is not None:
                                best_hunter["confidence_score"] = verif_data["confidence_score"]
                except requests.RequestException as e:
                    print(f"[Enrich] Prospeo verify request exception: {e}")
            elif domain:
                # (a) Find decision-makers for domain when Hunter found none
                providers_tried.append("prospeo")
                self.stats["provider_calls"]["prospeo"] += 1
                try:
                    prospeo_results = prospeo_client.find_decision_makers(domain)
                    if isinstance(prospeo_results, dict) and prospeo_results.get("error_status") in (401, 402, 429):
                        self._prospeo_disabled = True
                        print(f"[Enrich] Prospeo returned HTTP {prospeo_results['error_status']}; disabling provider for remainder of run.")
                    elif isinstance(prospeo_results, list):
                        for p in prospeo_results:
                            em_val = p.get("email")
                            if not em_val or "@" not in em_val:
                                continue
                            norm_v = normalize_verification(p.get("verification_status"))
                            if norm_v == "invalid":
                                continue
                            pos = p.get("title")
                            tier, norm_role = classify_title(pos)
                            if tier <= 7:
                                candidates.append({
                                    "email": em_val.strip().lower(),
                                    "full_name": p.get("full_name"),
                                    "title": pos or norm_role,
                                    "source": "prospeo",
                                    "confidence_score": p.get("confidence_score"),
                                    "verification_status": norm_v,
                                    "email_kind": "person",
                                    "tier": tier,
                                })
                except requests.RequestException as e:
                    print(f"[Enrich] Prospeo search request exception: {e}")

        # =========================================================================
        # 3. Apify fallback
        # =========================================================================
        person_candidates = [c for c in candidates if c["email_kind"] == "person"]
        if not person_candidates:
            scraped_items = None
            if apify_items is not None:
                scraped_items = apify_items
            elif self.apify and website:
                providers_tried.append("apify")
                self.stats["provider_calls"]["apify"] += 1
                try:
                    scraped_items = self.apify.run_contact_scraper([website])
                except Exception as e:
                    print(f"[Enrich] Apify run exception: {e}")

            if scraped_items:
                if "apify" not in providers_tried:
                    providers_tried.append("apify")
                for item in scraped_items:
                    item_dom = item.get("domain") or db.bare_domain(item.get("originalStartUrl") or item.get("url") or "")
                    if domain and db.bare_domain(item_dom) != domain:
                        continue
                    emails = item.get("emails", [])
                    for em in emails:
                        em_clean = em.strip().lower()
                        if "@" not in em_clean or em_clean == "no_email_found":
                            continue
                        local_p, em_dom = em_clean.split("@", 1)
                        em_dom = em_dom.removeprefix("www.")

                        # Drop foreign domain addresses
                        if domain and em_dom != domain and not em_dom.endswith("." + domain):
                            continue
                        # Drop placeholder email domains
                        if em_dom in PLACEHOLDER_EMAIL_DOMAINS:
                            continue
                        # Drop non-hiring inboxes
                        if any(term in local_p for term in NON_HIRING_INBOXES):
                            continue

                        # Classify departmental vs generic vs person
                        if local_p in DEPARTMENTAL_INBOXES or any(local_p.startswith(f"{d}+") or local_p.startswith(f"{d}-") or local_p == d for d in DEPARTMENTAL_INBOXES):
                            kind = "departmental"
                            tier = 8
                            title = "Departmental Inbox"
                        elif local_p in GENERIC_INBOXES or any(local_p.startswith(f"{g}+") or local_p.startswith(f"{g}-") or local_p == g for g in GENERIC_INBOXES):
                            kind = "generic"
                            tier = 9
                            title = "Generic Inbox"
                        else:
                            kind = "person"
                            tier = 7
                            title = None

                        candidates.append({
                            "email": em_clean,
                            "full_name": None,
                            "title": title,
                            "source": "apify",
                            "confidence_score": None,
                            "verification_status": "unknown",
                            "email_kind": kind,
                            "tier": tier,
                        })

        # =========================================================================
        # Deduplication & Ranking
        # =========================================================================
        # Deduplicate candidates by email (case-insensitive)
        deduped = {}
        for c in candidates:
            em = c["email"].lower()
            if em not in deduped:
                deduped[em] = c
            else:
                # Keep the one with better ranking
                if rank_key(c) < rank_key(deduped[em]):
                    deduped[em] = c

        all_candidates = list(deduped.values())

        # Check existing primary contact
        existing_primary = db.get_primary_contact(self.conn, company_id)
        manual_primary = (existing_primary is not None and existing_primary["source"] == "manual")

        # Pick best eligible candidate (person or departmental; generic is NEVER primary)
        primary_eligible = [c for c in all_candidates if c["email_kind"] in ("person", "departmental")]
        best_candidate = min(primary_eligible, key=rank_key) if primary_eligible else None

        # =========================================================================
        # Persistence via db contract
        # =========================================================================
        contacts_added = 0
        for c in all_candidates:
            is_best = (c == best_candidate)
            make_primary = (is_best and not manual_primary)
            try:
                db.add_contact(
                    self.conn,
                    company_id,
                    email=c["email"],
                    full_name=c["full_name"],
                    title=c["title"],
                    source=c["source"],
                    confidence_score=c["confidence_score"],
                    verification_status=c["verification_status"],
                    email_kind=c["email_kind"],
                    make_primary=make_primary
                )
                contacts_added += 1
            except Exception as e:
                print(f"[Enrich] Error adding contact {c['email']}: {e}")

        self.stats["contacts_added"] += contacts_added

        # Determine outcome and company status/notes updates
        if not all_candidates:
            db.update_company(self.conn, company_id, status="Skipped", notes="no_contact_found")
            outcome = "no_contact_found"
            primary_email = existing_primary["email"] if existing_primary else None
            primary_title = existing_primary["title"] if existing_primary else None
            self.stats["outcomes"]["no_contact_found"] += 1
        elif not primary_eligible:
            # Only generic inboxes found
            db.update_company(self.conn, company_id, status="Pending", notes="generic_inbox_only")
            outcome = "generic_inbox_only"
            primary_email = existing_primary["email"] if existing_primary else None
            primary_title = existing_primary["title"] if existing_primary else None
            self.stats["outcomes"]["generic_inbox_only"] += 1
        else:
            if manual_primary:
                outcome = "manual_primary_preserved"
                primary_email = existing_primary["email"]
                primary_title = existing_primary["title"]
                self.stats["outcomes"]["manual_primary_preserved"] += 1
            else:
                outcome = f"enriched_{best_candidate['email_kind']}"
                primary_email = best_candidate["email"]
                primary_title = best_candidate["title"]
                if best_candidate["email_kind"] == "person":
                    self.stats["outcomes"]["enriched_person"] += 1
                else:
                    self.stats["outcomes"]["enriched_departmental"] += 1

        summary = {
            "company_id": company_id,
            "contacts_added": contacts_added,
            "primary_email": primary_email,
            "primary_title": primary_title,
            "providers_tried": providers_tried,
            "outcome": outcome,
        }

        print(
            f"[Enrich] '{company_name}' (id={company_id}): outcome={outcome} | "
            f"primary={primary_email or 'None'} ({primary_title or 'None'}) | "
            f"contacts_added={contacts_added} | providers={providers_tried}"
        )
        return summary

    def run(self, limit=10, statuses=("Pending",), company_ids=None, refresh=False, dry_run=False) -> list[dict]:
        """
        Runs contact enrichment waterfall over matching companies.
        Skips companies that already have a person primary unless refresh=True.
        In dry_run: calls providers but writes nothing (transaction + rollback).
        """
        if dry_run:
            print("[Enrich] Mode: DRY-RUN (all database modifications will be rolled back).")
            self.conn.execute("SAVEPOINT dry_run_sp")

        results = []
        try:
            # 1. Fetch target companies
            if company_ids:
                companies = []
                for cid in company_ids:
                    row = db.get_company(self.conn, cid)
                    if row:
                        companies.append(row)
            else:
                companies = db.list_companies(self.conn, statuses=statuses)

            # 2. Filter companies
            to_process = []
            for comp in companies:
                self.stats["companies_evaluated"] += 1
                cid = comp["id"]
                primary = db.get_primary_contact(self.conn, cid)
                if not refresh and primary and primary["email_kind"] == "person":
                    self.stats["companies_skipped_person_primary"] += 1
                    continue
                to_process.append(comp)
                if limit is not None and len(to_process) >= limit:
                    break

            self.stats["companies_processed"] = len(to_process)

            # 3. First pass: Hunter + Prospeo per company
            # Identify companies where neither produced a person contact
            needing_apify = []
            for comp in to_process:
                # We can check website and domain
                web = comp["website"] or ""
                dom = comp["domain"] or ""
                cid = comp["id"]
                cname = comp["name"]

                if not web:
                    web, dom = self._resolve_missing_website(cid, cname)

                # Execute enrichment for comp
                # If Hunter and Prospeo don't produce person contact and Apify is available,
                # we delay Apify to a single batch run across all such companies
                # Let's run enrich_company with apify_items=[] if we plan to batch later:
                # Or run Hunter/Prospeo directly!
                res = self.enrich_company(comp, apify_items=[])
                # Check if person contact was found
                if res["outcome"] not in ("enriched_person", "manual_primary_preserved"):
                    needing_apify.append((comp, res))
                else:
                    results.append(res)

            # 4. Apify batch fallback for companies that yielded no person contact
            if needing_apify and self.apify and not self._apify_disabled:
                urls_to_crawl = []
                for comp, _ in needing_apify:
                    w = comp["website"] or ""
                    # Refresh company row in case website was resolved via Exa in pass 1
                    updated_row = db.get_company(self.conn, comp["id"])
                    if updated_row and updated_row["website"]:
                        w = updated_row["website"]
                    if w:
                        urls_to_crawl.append(w)

                urls_to_crawl = list(dict.fromkeys(urls_to_crawl)) # unique URLs
                if urls_to_crawl:
                    print(f"[Enrich] Batching {len(urls_to_crawl)} URLs into one Apify scrape run...")
                    self.stats["provider_calls"]["apify"] += 1
                    try:
                        scraped_data = self.apify.run_contact_scraper(urls_to_crawl)
                    except Exception as e:
                        print(f"[Enrich] Apify batch scrape failed: {e}")
                        scraped_data = []

                    # Re-run enrichment using the scraped dataset
                    for comp, _ in needing_apify:
                        updated_row = db.get_company(self.conn, comp["id"])
                        res = self.enrich_company(updated_row or comp, apify_items=scraped_data)
                        results.append(res)
                else:
                    for _, r in needing_apify:
                        results.append(r)
            else:
                for _, r in needing_apify:
                    results.append(r)

            # 5. Print final credits / usage summary
            print("\n[Enrich] ==================== Enrichment Summary ====================")
            print(f"[Enrich] Total companies evaluated:  {self.stats['companies_evaluated']}")
            print(f"[Enrich] Companies processed:        {len(results)}")
            print(f"[Enrich] Skipped (has person prim.): {self.stats['companies_skipped_person_primary']}")
            print("[Enrich] Outcomes:")
            for out_key, count in self.stats["outcomes"].items():
                print(f"[Enrich]   {out_key:25}: {count}")
            print("[Enrich] Provider calls:")
            for p_key, calls in self.stats["provider_calls"].items():
                disabled_note = " (DISABLED)" if getattr(self, f"_{p_key}_disabled", False) else ""
                print(f"[Enrich]   {p_key:10}: {calls}{disabled_note}")
            print(f"[Enrich] Total contacts added:        {self.stats['contacts_added']}")
            print(f"[Enrich] Mode:                       {'DRY-RUN' if dry_run else 'LIVE'}")
            print("[Enrich] =============================================================\n")

            return results
        finally:
            if dry_run:
                self.conn.execute("ROLLBACK TO SAVEPOINT dry_run_sp")
                self.conn.execute("RELEASE SAVEPOINT dry_run_sp")
                print("[Enrich] Dry-run rollback complete: database is untouched.")


def main(argv=None):
    """CLI: --limit N --refresh --dry-run --company NAME"""
    parser = argparse.ArgumentParser(description="Decision-maker contact enrichment waterfall")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of companies to enrich")
    parser.add_argument("--refresh", action="store_true", help="Re-enrich companies even if they already have a person primary")
    parser.add_argument("--dry-run", action="store_true", help="Call providers but roll back all database writes")
    parser.add_argument("--company", type=str, default=None, help="Process a specific company by name")
    parser.add_argument("--status", type=str, default="Pending", help="Company status filter (default: Pending)")
    args = parser.parse_args(argv)

    conn = db.connect()
    company_ids = None
    if args.company:
        comp = db.get_company_by_name(conn, args.company)
        if not comp:
            print(f"[Enrich] Company '{args.company}' not found.")
            return 1
        company_ids = [comp["id"]]

    enricher = ContactEnricher(conn)
    enricher.run(
        limit=args.limit,
        statuses=(args.status,),
        company_ids=company_ids,
        refresh=args.refresh,
        dry_run=args.dry_run
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
