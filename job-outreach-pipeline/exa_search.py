import json
import requests
from config import config

EMPLOYER_SCHEMA = {
    "type": "object",
    "properties": {
        "companies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "website": {"type": "string"},
                    "hq_location": {"type": "string"},
                    "company_type": {
                        "type": "string",
                        "enum": ["general_startup", "consultancy", "fintech", "isp", "bank", "ai"]
                    },
                    "ghana_eligibility": {
                        "type": "string",
                        "enum": ["ghana_based", "explicit_ghana", "africa_region", "worldwide"]
                    },
                    "evidence_url": {"type": "string"}
                },
                "required": ["name", "website", "company_type", "ghana_eligibility", "evidence_url"]
            }
        }
    },
    "required": ["companies"]
}

VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "official_website": {"type": "string"},
        "ghana_eligible": {
            "type": "string",
            "enum": ["yes_named", "yes_africa_or_emea", "yes_worldwide", "no", "unclear"]
        },
        "evidence_url": {"type": "string"},
        "careers_url": {"type": "string"},
        "note": {"type": "string"}
    },
    "required": ["ghana_eligible", "note"]
}

class ExaSearch:
    def __init__(self):
        self.api_key = config.get("EXA_API_KEY")
        self.total_cost = 0
        if not self.api_key:
            raise ValueError("EXA_API_KEY is missing in environment.")
            
    def search_companies(self, query, num_results=15):
        """
        Searches for pages matching the query and returns a list of results.
        Each result contains title, url, author, highlights, text.
        """
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "type": "auto",
            "numResults": num_results,
            "contents": {
                "text": True
            }
        }
        
        print(f"[Exa] Searching for: '{query}'...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print(f"[Exa] Found {len(results)} search results.")
                return results
            else:
                print(f"[Exa] Search failed: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"[Exa] Exception during search: {e}")
            return []
            
    def _structured_search(self, query, system_prompt, schema):
        """
        Runs a search whose answer is synthesized by Exa into output.content matching schema.
        Returns the content dict, or None on failure.
        """
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "type": "auto",
            "systemPrompt": system_prompt,
            "outputSchema": schema,
            "contents": {
                "highlights": True
            }
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=180)
            if response.status_code != 200:
                print(f"[Exa] Search failed: {response.status_code} - {response.text}")
                return None
            data = response.json()
            content = (data.get("output") or {}).get("content") or {}
            if isinstance(content, str):
                content = json.loads(content)
            self.total_cost += (data.get("costDollars") or {}).get("total", 0)
            return content
        except Exception as e:
            print(f"[Exa] Exception during search: {e}")
            return None

    def find_employers(self, query, system_prompt):
        """
        Searches for real employers matching the query and returns a list of companies
        with website, location, type and hiring evidence.
        """
        print(f"[Exa] Searching for employers: '{query}'...")
        content = self._structured_search(query, system_prompt, EMPLOYER_SCHEMA)
        companies = (content or {}).get("companies", [])
        print(f"[Exa] Found {len(companies)} employers.")
        return companies

    def verify_remote_hiring(self, company_name, website):
        """
        Checks the company's own careers pages for whether remote engineers based in Ghana are eligible.
        Returns a dict with ghana_eligible, evidence_url, careers_url, official_website and note.
        """
        system_prompt = (
            f"You are verifying whether {company_name} ({website}) currently hires remote engineers who live in Ghana. "
            "Prefer the company's own careers page, ATS job posts (Greenhouse, Lever, Ashby, Workable) or remote-hiring policy. "
            "Answer no if its remote roles are restricted to the US, Canada, Europe, UK or other regions that exclude Ghana. "
            "Answer unclear if the pages do not state where remote hires may live; never guess. "
            "note: one sentence quoting or paraphrasing the location rule you found."
        )
        content = self._structured_search(
            f"{company_name} careers remote engineer location requirements", system_prompt, VERIFY_SCHEMA)
        return content or {"ghana_eligible": "unclear", "note": "Verification search failed."}

    def company_summary(self, website):
        """
        Fetches a summary of the company's product, customers, and tech stack from its website using Exa's contents endpoint.
        """
        if not website:
            return ""
        url = "https://api.exa.ai/contents"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        summary_query = "What does this company do, what products/services do they build, who are their customers, and what is their tech stack?"
        payload = {
            "urls": [website],
            "summary": {
                "query": summary_query
            }
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results and results[0].get("summary"):
                    return results[0]["summary"].strip()
                # fallback: check statuses or other result properties
                return ""
            else:
                print(f"[Exa] Summary retrieval failed: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            print(f"[Exa] Exception during company summary retrieval: {e}")
            return ""

