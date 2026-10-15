"""
Decision-maker enrichment waterfall (Workstream B).

Waterfall per company:
1. Hunter.io Domain Search (type=personal, filter target roles)
2. Prospeo (find decision-makers if Hunter empty, and/or verify Hunter's best email)
3. Exa people search for named leaders/hiring staff (names only), then Hunter Email Finder for the best two
4. Apify fallback (batch URLs, classify departmental vs generic, drop non-hiring/foreign)
"""

import os
import sys
import re
import time
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
HUNTER_EMAIL_FINDER_PATH = "/email-finder"
HUNTER_MIN_FINDER_SCORE = 70  # below this (and unverified) a found address is a guess, and guesses bounce

PROSPEO_BASE_URL = "https://api.prospeo.io"
PROSPEO_SEARCH_PERSON_PATH = "/search-person"
PROSPEO_ENRICH_PERSON_PATH = "/enrich-person"
PROSPEO_MAX_LOOKUPS = 2  # per company, on the free plan's 100 credits
PROSPEO_MIN_INTERVAL = 3.1  # seconds between requests; the free plan allows 1/s, 20/min and 50/day
PROSPEO_RETRY_WAIT = 20  # one retry after a 429 before giving up on Prospeo for the run

NON_HIRING_INBOXES = [
    "support", "sales", "privacy", "press", "media", "legal", "noreply", "no-reply",
    "billing", "abuse", "security", "dpo", "compliance", "complaints", "fraud",
    "help", "investor", "training", "comms", "sellers", "marketing", "autoed"
]

PLACEHOLDER_EMAIL_DOMAINS = [
    "yourcompany.com", "example.com", "domain.com", "email.com", "company.com",
    "youremail.com", "yourdomain.com"
]

# Shared-inbox vocabulary lives in db so the v3 migration and the enricher classify addresses the same way
DEPARTMENTAL_INBOXES = db.DEPARTMENTAL_INBOXES
GENERIC_INBOXES = db.GENERIC_INBOXES

NON_HIRING_TITLE_PATTERN = re.compile(
    r"\b(sales|marketing|support|finance|legal|operations|operational|customer\s+success|account|accounting|accountant)\b",
    re.IGNORECASE
)


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
    7. (Reserved for Departmental Inbox)
    8. Other person contacts
    9. Non-hiring title (sales, marketing, support, etc. - stored as contact, never primary)
    """
    if not title:
        return 8, "Other Person"
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
        re.search(r"\btalent\s+(director|manager|lead|partner)\b", t) or
        re.search(r"head\s+of\s+(people|hr|human\s+resources)", t) or
        re.search(r"\b(hr|human\s+resources|people)\s+(director|manager|lead|business\s+partner)\b", t) or
        re.search(r"\b(recruiter|recruiting\s+manager|recruitment\s+manager)\b", t) or
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

    # Tier 9: Non-hiring title (sales, marketing, support, finance, legal, operations, etc.)
    if NON_HIRING_TITLE_PATTERN.search(t):
        return 9, title

    # Tier 8: Other person contacts
    return 8, "Other Person"


def rank_key(contact):
    """
    Sort key for candidate ranking (lower = better):
    Tie-break on verification ('valid' > 'accept_all' > 'unknown'/None; drop 'invalid') then confidence.
    """
    verif_order = {"valid": 1, "accept_all": 2, "unknown": 3}
    v_score = verif_order.get(contact.get("verification_status"), 3)
    conf = contact.get("confidence_score")
    conf_score = -int(conf) if conf is not None else 0
    return (contact.get("tier", 8), v_score, conf_score)


class ProspeoClient:
    """
    Prospeo API adapter class.
    Endpoints and base URL are module constants. Authenticates via X-KEY header.
    """
    def __init__(self, api_key=None, session=None, base_url=PROSPEO_BASE_URL, timeout=15,
                 min_interval=None, retry_wait=None):
        self.api_key = api_key
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.min_interval = PROSPEO_MIN_INTERVAL if min_interval is None else min_interval
        self.retry_wait = PROSPEO_RETRY_WAIT if retry_wait is None else retry_wait
        self._last_call = 0.0

    def _post(self, url, payload):
        """POST spaced at least min_interval apart, retrying once after a 429."""
        for attempt in range(2):
            wait = self.min_interval - (time.monotonic() - self._last_call)
            if wait > 0:
                time.sleep(wait)
            res = self.session.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
            self._last_call = time.monotonic()
            if res.status_code != 429 or attempt == 1:
                return res
            print(f"[Enrich] Prospeo rate limit hit; waiting {self.retry_wait}s and retrying once.")
            time.sleep(self.retry_wait)
        return res

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
        res = self._post(url, payload)
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return []

        data = res.json()
        contacts = []
        lookups_left = PROSPEO_MAX_LOOKUPS  # each email lookup costs a credit; spend them on hiring decision-makers only

        items = data.get("results") or data.get("data") or data.get("response") or data.get("emails") or []
        if isinstance(items, list):
            for item in items:
                p = item.get("person", item) if isinstance(item, dict) else {}
                if not isinstance(p, dict):
                    continue

                em_field = p.get("email") or p.get("work_email") or ""
                em_str = ""
                verif_status = "unknown"
                if isinstance(em_field, dict):
                    em_str = em_field.get("email") or ""  # null when Prospeo has no address for them
                    verif_status = em_field.get("status") or "unknown"
                elif isinstance(em_field, str):
                    em_str = em_field
                    verif_status = p.get("verification_status") or p.get("status") or "unknown"
                if "*" in em_str:
                    em_str = ""  # masked until revealed with a paid lookup; never store or send to it

                first = p.get("first_name") or ""
                last = p.get("last_name") or ""
                full_name = p.get("full_name") or f"{first} {last}".strip() or None
                title = p.get("current_job_title") or p.get("job_title") or p.get("title") or p.get("position")
                conf = p.get("confidence_score") or p.get("score") or p.get("confidence")

                person_id = p.get("person_id") or p.get("id")
                worth_a_lookup = classify_title(title)[0] <= 6 and lookups_left > 0
                if not em_str and worth_a_lookup and (person_id or (first and last)):
                    lookups_left -= 1
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

        res = self._post(url, {"data": data_payload})
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return {}

        data = res.json()
        resp_obj = data.get("person") or data.get("response") or data.get("data") or data
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
        res = self._post(url, {"data": {"email": email}})
        if res.status_code in (401, 402, 429):
            return {"error_status": res.status_code}
        if res.status_code != 200:
            return {}
        data = res.json()
        resp_obj = data.get("person") or data.get("response") or data.get("data") or data
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
        self._refresh = False
        self._notices_printed = set()

        self.stats = {
            "companies_evaluated": 0,
            "companies_processed": 0,
            "companies_skipped_person_primary": 0,
            "outcomes": {
                "enriched_person": 0,
                "enriched_departmental": 0,
                "generic_inbox_only": 0,
                "people_found_no_email": 0,
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

    def _check_configured(self, provider_name, key):
        """Prints unconfigured notice at most once per run."""
        if not is_configured(key):
            if provider_name not in self._notices_printed:
                print(f"[Enrich] {provider_name.capitalize()} API key not configured or placeholder; skipping.")
                self._notices_printed.add(provider_name)
            return False
        return True

    @property
    def apify(self):
        if self._apify is None and not self._apify_disabled:
            token = config.get("APIFY_API_TOKEN")
            if not self._check_configured("apify", token):
                self._apify_disabled = True
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
            if not self._check_configured("exa", key):
                self._exa_disabled = True
                return None
            try:
                self._exa = ExaSearch()
            except Exception as e:
                self._exa_disabled = True
                print(f"[Enrich] Could not initialize ExaSearch: {e}")
                return None
        return self._exa

    def _resolve_website(self, company) -> tuple[str, str]:
        """Resolves company website and domain once; updates DB if found."""
        company_id = company["id"]
        company_name = company["name"]
        website = company["website"] or ""
        domain = company["domain"] or ""

        if not website:
            if self.exa and not self._exa_disabled:
                print(f"[Enrich] Website missing for '{company_name}'. Searching via Exa...")
                self.stats["provider_calls"]["exa"] += 1
                try:
                    results = self.exa.search_companies(f"{company_name} official website homepage", num_results=1)
                    if results and results[0].get("url"):
                        parsed = urllib.parse.urlparse(results[0]["url"])
                        website = f"{parsed.scheme}://{parsed.netloc}".lower()
                        domain = db.bare_domain(website)
                        db.update_company(self.conn, company_id, website=website, domain=domain)
                        print(f"[Enrich] Resolved website for '{company_name}': {website}")
                except Exception as e:
                    print(f"[Enrich] Exa search failed for '{company_name}': {e}")
        elif not domain:
            domain = db.bare_domain(website)
            db.update_company(self.conn, company_id, domain=domain)

        return website, domain

    def _collect_api_candidates(self, company, website, domain) -> tuple[list[dict], list[str]]:
        """
        Executes Hunter and Prospeo once for a company.
        Returns (candidates, providers_tried).
        """
        providers_tried = []
        candidates = []

        # 1. Hunter.io Domain Search
        if self._check_configured("hunter", self.hunter_key):
            if self._hunter_disabled:
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

                            # Non-hiring title: store as contact, never primary
                            can_be_primary = (tier != 9)

                            candidates.append({
                                "email": val.strip().lower(),
                                "full_name": full_name,
                                "title": pos or norm_role,
                                "source": "hunter",
                                "confidence_score": em.get("confidence"),
                                "verification_status": norm_v,
                                "email_kind": "person",
                                "tier": tier,
                                "can_be_primary": can_be_primary,
                            })
                    else:
                        print(f"[Enrich] Hunter returned HTTP {res.status_code}: {res.text}")
                except requests.RequestException as e:
                    print(f"[Enrich] Hunter request exception: {e}")

        # 2. Prospeo
        if self._check_configured("prospeo", self.prospeo_key):
            if self._prospeo_disabled:
                print("[Enrich] Prospeo provider disabled for this run; skipping.")
            else:
                prospeo_client = ProspeoClient(self.prospeo_key, session=self.session)
                if candidates:
                    # Verify Hunter's best email
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
                    # Find decision-makers for domain when Hunter found none
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
                                can_be_primary = (tier != 9)
                                candidates.append({
                                    "email": em_val.strip().lower(),
                                    "full_name": p.get("full_name"),
                                    "title": pos or norm_role,
                                    "source": "prospeo",
                                    "confidence_score": p.get("confidence_score"),
                                    "verification_status": norm_v,
                                    "email_kind": "person",
                                    "tier": tier,
                                    "can_be_primary": can_be_primary,
                                })
                    except requests.RequestException as e:
                        print(f"[Enrich] Prospeo search request exception: {e}")

        return candidates, providers_tried

    def _find_named_people(self, company, domain, candidates) -> tuple[list[dict], list[dict], list[str]]:
        """
        Runs only when no hiring decision-maker with an email turned up. Asks Exa for named engineering leaders,
        hiring staff and founders, then, if Hunter is configured, looks up a verified email for the best two.
        Addresses are never guessed. Returns (people, new_candidates, providers_tried).
        """
        if any(c["tier"] <= 6 and c.get("can_be_primary", False) for c in candidates):
            return [], [], []
        if not domain or not self.exa or self._exa_disabled:
            return [], [], []
        if db.list_people(self.conn, company["id"]) and not self._refresh:
            return [], [], []  # names already found on an earlier run; review them instead of paying again
        self.stats["provider_calls"]["exa"] += 1
        try:
            found = self.exa.find_people(company["name"], domain)
        except Exception as e:
            print(f"[Enrich] Exa people search failed: {e}")
            return [], [], ["exa"]

        people = []
        for p in found if isinstance(found, list) else []:
            title = (p.get("title") or "").strip() or None
            tier, _ = classify_title(title)
            if tier == 9:
                continue  # sales, marketing, support: not who decides on an engineering hire
            people.append({"full_name": p["name"].strip(), "title": title,
                           "profile_url": p.get("profile_url") or None, "tier": tier})
        people.sort(key=lambda p: p["tier"])

        providers = ["exa"]
        new_candidates = []
        known = {(c.get("full_name") or "").lower() for c in candidates}
        targets = [p for p in people
                   if p["tier"] <= 6 and len(p["full_name"].split()) >= 2 and p["full_name"].lower() not in known][:2]
        if targets and self._check_configured("hunter", self.hunter_key) and not self._hunter_disabled:
            providers.append("hunter")
            for p in targets:
                cand = self._hunter_find_email(domain, p)
                if cand:
                    new_candidates.append(cand)
        return people, new_candidates, providers

    def _hunter_find_email(self, domain, person):
        """Hunter Email Finder for one named person. Returns a candidate only for a verified or high-score address."""
        if self._hunter_disabled:
            return None
        self.stats["provider_calls"]["hunter"] += 1
        try:
            res = self.session.get(
                f"{HUNTER_BASE_URL}{HUNTER_EMAIL_FINDER_PATH}",
                params={"domain": domain, "full_name": person["full_name"], "api_key": self.hunter_key},
                timeout=15,
            )
        except requests.RequestException as e:
            print(f"[Enrich] Hunter email-finder request exception: {e}")
            return None
        if res.status_code in (401, 402, 429):
            self._hunter_disabled = True
            print(f"[Enrich] Hunter returned HTTP {res.status_code}; disabling provider for remainder of run.")
            return None
        if res.status_code != 200:
            return None
        data = (res.json() or {}).get("data") or {}
        email = data.get("email")
        if not email or "@" not in email:
            return None
        verif = data.get("verification")
        v_status = normalize_verification(verif.get("status") if isinstance(verif, dict) else verif)
        score = data.get("score")
        if v_status == "invalid" or (v_status != "valid" and (score or 0) < HUNTER_MIN_FINDER_SCORE):
            return None
        return {
            "email": email.strip().lower(),
            "full_name": person["full_name"],
            "title": person["title"],
            "source": "hunter",
            "confidence_score": score,
            "verification_status": v_status,
            "email_kind": "person",
            "tier": person["tier"],
            "can_be_primary": True,
        }

    def _stored_apify_candidates(self, company_id) -> list[dict]:
        """Contacts from an earlier website scrape, in candidate form, so a re-run ranks them without re-scraping."""
        tiers = {"departmental": (7, True), "generic": (10, False), "person": (8, True)}
        out = []
        for c in db.list_contacts(self.conn, company_id):
            if c["source"] != "apify":
                continue
            tier, can_be_primary = tiers.get(c["email_kind"] or "generic", (10, False))
            out.append({
                "email": c["email"], "full_name": c["full_name"], "title": c["title"], "source": "apify",
                "confidence_score": c["confidence_score"], "verification_status": c["verification_status"] or "unknown",
                "email_kind": c["email_kind"] or "generic", "tier": tier, "can_be_primary": can_be_primary,
            })
        return out

    def _collect_apify_candidates(self, company, domain, scraped_items) -> tuple[list[dict], list[str]]:
        """
        Parses pre-scraped Apify dataset items for a company's domain.
        Returns (candidates, providers_tried).
        """
        candidates = []
        providers_tried = ["apify"] if scraped_items else []

        if not scraped_items:
            return candidates, providers_tried

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

                # Classify departmental vs generic vs person (an address only counts as a person if it reads like a name)
                kind = db.classify_address(em_clean, domain)
                if kind == "departmental":
                    tier = 7  # Departmental inbox ranks above Other Person (Tier 8)
                    title = "Departmental Inbox"
                    can_be_primary = True
                elif kind == "generic":
                    tier = 10
                    title = "Generic Inbox"
                    can_be_primary = False  # NEVER primary
                else:
                    tier = 8  # Other person contact
                    title = None
                    can_be_primary = True

                candidates.append({
                    "email": em_clean,
                    "full_name": None,
                    "title": title,
                    "source": "apify",
                    "confidence_score": None,
                    "verification_status": "unknown",
                    "email_kind": kind,
                    "tier": tier,
                    "can_be_primary": can_be_primary,
                })

        return candidates, providers_tried

    def _persist(self, company, candidates, providers_tried, people=()) -> dict:
        """
        Persists contacts and updates company status/notes once per company.
        Returns summary dict.
        """
        company_id = company["id"]
        company_name = company["name"]
        curr_status = company["status"]
        curr_notes = company["notes"] or ""

        # Deduplicate candidates by email (case-insensitive)
        deduped = {}
        for c in candidates:
            em = c["email"].lower()
            if em not in deduped:
                deduped[em] = c
            else:
                if rank_key(c) < rank_key(deduped[em]):
                    deduped[em] = c

        all_candidates = list(deduped.values())

        # Check existing primary contact
        existing_primary = db.get_primary_contact(self.conn, company_id)
        manual_primary = (existing_primary is not None and existing_primary["source"] == "manual")

        # Pick best eligible candidate (generic and non-hiring titles are NEVER primary)
        primary_eligible = [c for c in all_candidates if c.get("can_be_primary", False)]
        best_candidate = min(primary_eligible, key=rank_key) if primary_eligible else None

        # Add contacts via db contract
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

        # Named people, linked to their contact when an email for them was found
        email_by_name = {(c["full_name"] or "").lower(): c["email"] for c in all_candidates if c.get("full_name")}
        for p in people:
            contact_id = None
            email = email_by_name.get(p["full_name"].lower())
            if email:
                row = db.find_contact_by_email(self.conn, email)
                contact_id = row["id"] if row else None
            db.add_person(self.conn, company_id, p["full_name"], title=p["title"],
                          profile_url=p["profile_url"], source="exa", contact_id=contact_id)

        # STATUS SCOPE:
        # Only change company status when currently Pending or Skipped(no_contact_found / generic_inbox_only)
        status_modifiable = (curr_status == "Pending") or (
            curr_status == "Skipped" and curr_notes in ("no_contact_found", "generic_inbox_only", "people_found_no_email")
        )

        # Names found on this run or an earlier one
        has_people = bool(people) or bool(db.list_people(self.conn, company_id))

        if not all_candidates and not has_people:
            outcome = "no_contact_found"
            primary_email = existing_primary["email"] if existing_primary else None
            primary_title = existing_primary["title"] if existing_primary else None
            self.stats["outcomes"]["no_contact_found"] += 1
            if status_modifiable:
                db.update_company(self.conn, company_id, status="Skipped", notes="no_contact_found")
        elif not primary_eligible and has_people:
            # Named decision-makers but no usable address for them: stays Pending so one can be added in review
            outcome = "people_found_no_email"
            primary_email = existing_primary["email"] if existing_primary else None
            primary_title = existing_primary["title"] if existing_primary else None
            self.stats["outcomes"]["people_found_no_email"] += 1
            if status_modifiable:
                db.update_company(self.conn, company_id, status="Pending", notes="people_found_no_email")
        elif not primary_eligible:
            # Only generic inboxes or non-hiring titles found
            outcome = "generic_inbox_only"
            primary_email = existing_primary["email"] if existing_primary else None
            primary_title = existing_primary["title"] if existing_primary else None
            self.stats["outcomes"]["generic_inbox_only"] += 1
            if status_modifiable:
                db.update_company(self.conn, company_id, status="Pending", notes="generic_inbox_only")
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

            if status_modifiable:
                fields = {}
                if curr_status != "Pending":
                    fields["status"] = "Pending"
                if curr_notes in ("no_contact_found", "generic_inbox_only", "people_found_no_email"):
                    fields["notes"] = ""
                if fields:
                    db.update_company(self.conn, company_id, **fields)

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
            f"contacts_added={contacts_added} | people={len(people)} | providers={providers_tried}"
        )
        return summary

    def enrich_company(self, company_row, apify_items=None) -> dict:
        """
        Executes waterfall for a single company row (Row or dict).
        Returns:
            {"company_id", "contacts_added", "primary_email", "primary_title", "providers_tried", "outcome"}
        """
        website, domain = self._resolve_website(company_row)
        fresh_row = db.get_company(self.conn, company_row["id"])
        comp = fresh_row or company_row

        candidates, providers_tried = self._collect_api_candidates(comp, website, domain)
        people, named_cands, people_provs = self._find_named_people(comp, domain, candidates)
        candidates.extend(named_cands)
        providers_tried.extend(p for p in people_provs if p not in providers_tried)

        # Apify fallback if no target person candidate found (Tiers 1-6)
        has_target_person = any(c["tier"] <= 6 and c.get("can_be_primary", False) for c in candidates)
        if not has_target_person or apify_items is not None:
            if apify_items is not None:
                apify_cand, apify_prov = self._collect_apify_candidates(comp, domain, apify_items)
                candidates.extend(apify_cand)
                for p in apify_prov:
                    if p not in providers_tried:
                        providers_tried.append(p)
            elif self.apify and website and not self._apify_disabled:
                providers_tried.append("apify")
                self.stats["provider_calls"]["apify"] += 1
                try:
                    scraped_data = self.apify.run_contact_scraper([website])
                    apify_cand, _ = self._collect_apify_candidates(comp, domain, scraped_data)
                    candidates.extend(apify_cand)
                except Exception as e:
                    print(f"[Enrich] Apify run exception: {e}")

        return self._persist(comp, candidates, providers_tried, people)

    def run(self, limit=10, statuses=("Pending",), company_ids=None, refresh=False, dry_run=False) -> list[dict]:
        """
        Runs contact enrichment waterfall over matching companies.
        Skips companies that already have a person primary unless refresh=True.
        In dry_run: calls providers but writes nothing (transaction + rollback).
        """
        self._refresh = refresh
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

            # 3. Resolve websites once for all companies
            company_data = []
            for comp in to_process:
                web, dom = self._resolve_website(comp)
                fresh_row = db.get_company(self.conn, comp["id"])
                company_data.append((fresh_row or comp, web, dom))

            # 4. Collect API candidates (Hunter + Prospeo) once per company
            per_company_data = {}
            needing_apify = []
            for comp, web, dom in company_data:
                cid = comp["id"]
                try:
                    cands, provs = self._collect_api_candidates(comp, web, dom)
                    people, named_cands, people_provs = self._find_named_people(comp, dom, cands)
                except Exception as e:
                    # One malformed provider response must not throw away the rest of the run
                    print(f"[Enrich] '{comp['name']}' skipped after an error: {type(e).__name__}: {e}")
                    continue
                cands.extend(named_cands)
                provs.extend(p for p in people_provs if p not in provs)
                per_company_data[cid] = {
                    "comp": comp,
                    "website": web,
                    "domain": dom,
                    "candidates": cands,
                    "providers_tried": provs,
                    "people": people,
                }
                has_target_person = any(c["tier"] <= 6 and c.get("can_be_primary", False) for c in cands)
                # A site that was already scraped returns the same inboxes again: reuse what is stored instead of
                # paying for another scrape, unless --refresh
                stored = self._stored_apify_candidates(cid)
                if not has_target_person:
                    if stored and not refresh:
                        cands.extend(stored)
                        if "apify" not in provs:
                            provs.append("apify")
                    else:
                        needing_apify.append(cid)

            # 5. One batched Apify run for companies lacking a person candidate
            if needing_apify and self.apify and not self._apify_disabled:
                urls_to_crawl = list(dict.fromkeys([
                    per_company_data[cid]["website"]
                    for cid in needing_apify
                    if per_company_data[cid]["website"]
                ]))
                if urls_to_crawl:
                    print(f"[Enrich] Batching {len(urls_to_crawl)} URLs into one Apify scrape run...")
                    self.stats["provider_calls"]["apify"] += 1
                    try:
                        scraped_data = self.apify.run_contact_scraper(urls_to_crawl)
                    except Exception as e:
                        print(f"[Enrich] Apify batch scrape failed: {e}")
                        scraped_data = []

                    for cid in needing_apify:
                        entry = per_company_data[cid]
                        apify_cand, apify_prov = self._collect_apify_candidates(entry["comp"], entry["domain"], scraped_data)
                        entry["candidates"].extend(apify_cand)
                        for p in apify_prov:
                            if p not in entry["providers_tried"]:
                                entry["providers_tried"].append(p)

            # 6. Persist each company exactly once
            for comp, _, _ in company_data:
                cid = comp["id"]
                if cid not in per_company_data:
                    continue
                entry = per_company_data[cid]
                fresh_row = db.get_company(self.conn, cid) or entry["comp"]
                summary = self._persist(fresh_row, entry["candidates"], entry["providers_tried"], entry["people"])
                results.append(summary)

            # 7. Print final credits / usage summary
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
