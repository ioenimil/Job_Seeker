import json
import re
import unicodedata
from datetime import datetime
import requests

import applicant
from config import config
import db
from exa_search import ExaSearch


def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def strip_control_and_html(text: str) -> str:
    """Strip HTML tags and unprintable/control characters."""
    if not text:
        return ""
    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", "", text)
    # Remove control characters except newline and tab
    cleaned = "".join(ch for ch in cleaned if unicodedata.category(ch)[0] != "C" or ch in ("\n", "\t"))
    return cleaned.strip()


def extract_numbers_metrics(text: str) -> list[str]:
    """
    Extract numbers, percentages, metrics like 74%, 96%, #1, 1st, 10, etc.
    """
    # Matches patterns like 74%, #1, 1st, 2nd, 10, etc.
    matches = re.findall(r"(?:#\d+|\b\d+(?:st|nd|rd|th)?%?|\b\d+/\d+)", text, re.IGNORECASE)
    return [m.lower() for m in matches]


KNOWN_TECH_WORDS = {
    "aws", "gcp", "azure", "docker", "kubernetes", "k8s", "terraform", "vault",
    "helm", "argo", "argocd", "argo-cd", "jenkins", "gitlab", "github", "kafka",
    "rabbitmq", "redis", "postgres", "postgresql", "mysql", "mongodb", "zilliz",
    "milvus", "pinecone", "qdrant", "weaviate", "fastapi", "flask", "django",
    "react", "vue", "angular", "nextjs", "nodejs", "python", "golang", "go",
    "rust", "typescript", "javascript", "prometheus", "grafana", "loki", "thanos",
    "jaeger", "opentelemetry", "otel", "guardduty", "cloudtrail", "cloudwatch",
    "keycloak", "copilotkit", "cube", "cube-core", "deepeval", "rag", "llm", "ai",
    "sso", "rbac", "vpc", "ec2", "spot", "ci/cd", "cicd", "gitops", "iac"
}


def extract_tech_and_proper_nouns(text: str) -> list[str]:
    """
    Extract technology/proper-noun tokens:
    capitalised words, CamelCase, tokens with digits, known tech words.
    """
    tokens = []
    # Tokenize words, keeping hyphens or slashes if inside a word
    words = re.findall(r"[A-Za-z0-9]+(?:[-_/][A-Za-z0-9]+)*", text)
    for w in words:
        w_lower = w.lower()
        is_cap = w[0].isupper() and not w.isupper()
        is_all_cap = w.isupper() and len(w) > 1
        is_camel = bool(re.search(r"[a-z][A-Z]", w))
        has_digit = any(c.isdigit() for c in w)
        is_tech = w_lower in KNOWN_TECH_WORDS
        if is_cap or is_all_cap or is_camel or has_digit or is_tech:
            tokens.append(w_lower)
    return tokens



def fallback_pitch(company_row) -> dict:
    """
    Deterministic fallback pitch using per-type static bullets from CoverLetterGenerator.
    """
    from cover_letter_generator import CoverLetterGenerator
    gen = CoverLetterGenerator()
    company_name = company_row["name"] if isinstance(company_row, (dict, db.sqlite3.Row)) else getattr(company_row, "name", "")
    company_type = company_row["company_type"] if isinstance(company_row, (dict, db.sqlite3.Row)) else getattr(company_row, "company_type", "")
    role_title = ""
    try:
        role_title = company_row["role_title"]
    except Exception:
        pass
    if not role_title:
        role_title = applicant.role_for(company_type)

    letter_content = gen.get_letter_content(company_name, role_title, company_type)
    bullets_out = []
    # Match the bullet text back to fact_id
    ach_by_title_or_text = {ach["text"].strip(): ach["id"] for ach in applicant.ACHIEVEMENTS}
    for title, text in letter_content["bullets"]:
        fid = ach_by_title_or_text.get(text.strip(), "fallback-fact")
        bullets_out.append({
            "fact_id": fid,
            "title": title,
            "text": text
        })

    return {
        "lead": letter_content["lead"],
        "bullets": bullets_out,
        "provider": "none",
        "model": "deterministic",
        "grounded": True,
        "fallback_reason": None,
        "generated_at": now_iso()
    }


def validate_pitch(pitch: dict, company) -> list[str]:
    """
    Grounding invariant validation:
    - exactly 3 bullets with distinct fact_ids that exist in ACHIEVEMENTS
    - every number/percentage/metric in a bullet appears in its source fact text
    - every technology/proper-noun token in a bullet appears in its source fact text (case-insensitive)
    - the company's stack may be mentioned in the LEAD only, never claimed as candidate experience in a bullet
    - no certification/degree/employer words unless present in FACT_SHEET/source
    - lead may only reference the company name and terms present in summary
    - length caps (bullet <= 320 chars, lead <= 300)
    Returns list of error messages (empty list if valid).
    """
    errors = []
    if not isinstance(pitch, dict):
        return ["Pitch must be a JSON dictionary."]

    lead = pitch.get("lead", "")
    bullets = pitch.get("bullets", [])

    if not isinstance(lead, str) or not lead.strip():
        errors.append("Lead must be a non-empty string.")
    elif len(lead) > 300:
        errors.append(f"Lead exceeds 300 characters ({len(lead)} chars).")

    if not isinstance(bullets, list) or len(bullets) != 3:
        errors.append(f"Bullets must contain exactly 3 items (found {len(bullets) if isinstance(bullets, list) else 0}).")
        return errors

    ach_map = {ach["id"]: ach for ach in applicant.ACHIEVEMENTS}
    fact_ids = [b.get("fact_id") for b in bullets if isinstance(b, dict)]

    if len(set(fact_ids)) != 3:
        errors.append(f"Bullets must have 3 distinct fact_ids (found {len(set(fact_ids))}).")

    for idx, b in enumerate(bullets):
        if not isinstance(b, dict):
            errors.append(f"Bullet {idx+1} is not an object.")
            continue
        fid = b.get("fact_id")
        title = b.get("title", "")
        text = b.get("text", "")

        if not fid or fid not in ach_map:
            errors.append(f"Bullet {idx+1} references unknown fact_id: '{fid}'.")
            continue

        if len(text) > 320:
            errors.append(f"Bullet {idx+1} exceeds 320 characters ({len(text)} chars).")

        source_ach = ach_map[fid]
        source_text = source_ach["text"]
        source_lower = source_text.lower()

        # Check metrics/numbers
        bullet_metrics = extract_numbers_metrics(text)
        source_metrics = set(extract_numbers_metrics(source_text))
        for m in bullet_metrics:
            if m not in source_metrics and m not in source_lower:
                errors.append(f"Bullet {idx+1} contains metric/number '{m}' not in source fact '{fid}'.")

        # Check tech and proper noun tokens
        # Common English stop words / sentence starters to not treat as proper nouns
        ignore_words = {
            "i", "at", "my", "we", "the", "in", "with", "and", "to", "for", "on", "a", "an",
            "as", "by", "of", "from", "into", "across", "over", "using", "built", "designed",
            "deployed", "architected", "operated", "won", "engineered", "secured", "integrated",
            "provisioned", "exceeded", "running", "scaling", "raising", "reducing", "cutting",
            "helping", "keeping", "delivering", "right-sizing", "implement", "run", "design"
        }
        b_tokens = extract_tech_and_proper_nouns(text)
        for tok in b_tokens:
            if tok in ignore_words:
                continue
            if tok not in source_lower:
                errors.append(f"Bullet {idx+1} claims technology/token '{tok}' not in source fact '{fid}'.")

    # Check certification/degree/employer words across all bullets
    # Only allowed if present in FACT_SHEET or source fact
    fact_sheet_str = json.dumps(applicant.FACT_SHEET).lower()
    restricted_terms = [
        "bachelor", "master", "phd", "degree", "certified", "certification",
        "aws solutions architect", "kcna", "knust", "amalitech", "turing", "boasoft",
        "google", "microsoft", "meta", "stanford", "mit", "harvard"
    ]
    for idx, b in enumerate(bullets):
        if not isinstance(b, dict):
            continue
        fid = b.get("fact_id")
        source_text = ach_map.get(fid, {}).get("text", "").lower()
        combined_source = (source_text + " " + fact_sheet_str).lower()
        b_lower = b.get("text", "").lower()
        for term in restricted_terms:
            if term in b_lower and term not in combined_source:
                errors.append(f"Bullet {idx+1} mentions restricted term '{term}' not present in fact sheet or source.")

    # Validate lead: lead may only reference the company name and terms present in summary
    company_name = ""
    summary = ""
    if isinstance(company, (dict, db.sqlite3.Row)):
        company_name = company.get("name", "") if isinstance(company, dict) else (company["name"] if "name" in company.keys() else "")
        summary = company.get("summary", "") if isinstance(company, dict) else (company["summary"] if "summary" in company.keys() else "")
    elif company:
        company_name = getattr(company, "name", "")
        summary = getattr(company, "summary", "")

    # Check lead terms
    # "lead may only reference the company name and terms present in summary"
    lead_clean = strip_control_and_html(lead)
    common_connectives = {
        "i", "at", "my", "we", "the", "in", "with", "and", "to", "for", "on", "a", "an",
        "as", "by", "of", "from", "into", "across", "over", "using", "built", "designed",
        "deployed", "architected", "operated", "won", "engineered", "secured", "integrated",
        "provisioned", "exceeded", "running", "scaling", "raising", "reducing", "cutting",
        "helping", "keeping", "delivering", "right-sizing", "implement", "run", "design",
        "is", "are", "was", "were", "be", "being", "been", "that", "this", "these", "those",
        "it", "its", "their", "our", "your", "what", "which", "who", "whom", "whose", "how",
        "when", "where", "why", "both", "all", "any", "some", "more", "most", "other",
        "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
        "can", "will", "just", "should", "now", "builds", "makes", "creates", "develops",
        "offers", "provides", "delivers", "focuses", "helps", "works", "powers", "operates",
        "systems", "system", "products", "product", "platform", "platforms", "services",
        "service", "technology", "technologies", "engineering", "team", "teams", "tools",
        "solution", "solutions", "applications", "application", "software", "infrastructure"
    }

    if summary:
        summary_lower = summary.lower()
        cname_lower = company_name.lower()
        lead_words = re.findall(r"[A-Za-z0-9]+(?:[-_][A-Za-z0-9]+)*", lead_clean)
        for w in lead_words:
            w_lower = w.lower()
            if w_lower in common_connectives:
                continue
            if w_lower not in summary_lower and w_lower not in cname_lower:
                errors.append(f"Lead references term '{w_lower}' not found in company summary or company name.")

    return errors




def _call_llm(provider: str, model: str, system_prompt: str, user_prompt: str) -> str:
    """Calls Anthropic, OpenAI, or Ollama via requests."""
    timeout = 60
    if provider == "anthropic":
        api_key = config.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is missing.")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": model,
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        content_blocks = data.get("content", [])
        text_out = "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text")
        return text_out

    elif provider == "openai":
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""

    elif provider == "ollama":
        host = config.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        url = f"{host}/api/chat"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "format": "json",
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", {}).get("content", "")

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _parse_pitch_json(raw_text: str) -> dict:
    """Strips markdown json wrappers and loads JSON."""
    cleaned = strip_control_and_html(raw_text)
    if "```json" in cleaned:
        cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in cleaned:
        cleaned = cleaned.split("```", 1)[1].split("```", 1)[0]
    return json.loads(cleaned.strip())


def build_pitch(company_row, provider=None) -> dict:
    """
    Builds a tailored grounded pitch for company_row.
    Keys: lead, bullets, provider, model, grounded: bool, fallback_reason|None, generated_at.
    """
    if provider is None:
        provider = config.get("LLM_PROVIDER", "none").lower().strip()
    else:
        provider = provider.lower().strip()

    if provider in ("none", "", None):
        return fallback_pitch(company_row)

    # Determine model
    if provider == "anthropic":
        model = config.get("LLM_MODEL", "claude-sonnet-5-5")
    elif provider in ("openai", "ollama"):
        model = config.get("LLM_MODEL")
        if not model:
            raise ValueError(f"LLM_MODEL is required when LLM_PROVIDER is '{provider}'")
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

    # Prepare inputs
    c_name = company_row["name"] if isinstance(company_row, (dict, db.sqlite3.Row)) else getattr(company_row, "name", "")
    c_site = company_row["website"] if isinstance(company_row, (dict, db.sqlite3.Row)) else getattr(company_row, "website", "")
    c_type = company_row["company_type"] if isinstance(company_row, (dict, db.sqlite3.Row)) else getattr(company_row, "company_type", "")
    c_summary = ""
    try:
        c_summary = company_row["summary"] or ""
    except Exception:
        c_summary = getattr(company_row, "summary", "") or ""

    system_prompt = (
        "You are an expert platform and AI engineer synthesizing a tailored cover letter pitch.\n"
        "You must respond ONLY with valid JSON with this exact schema:\n"
        "{\n"
        '  "lead": "1-2 sentence lead naming what the company actually does (from summary only, <= 300 chars)",\n'
        '  "bullets": [\n'
        '    {"fact_id": "kebab-id-from-achievements", "title": "Short Title", "text": "Rephrased bullet <= 320 chars"}\n'
        "  ]\n"
        "}\n"
        "Rules:\n"
        "1. Select EXACTLY 3 distinct achievements from the candidate's achievements bank.\n"
        "2. Grounding invariant: Every metric, number, and percentage in your bullet MUST appear in the source fact text.\n"
        "3. Every technology or proper noun in your bullet MUST appear in the source fact text. You may NEVER claim company's stack as candidate experience.\n"
        "4. No certification/degree/employer words unless present in candidate fact sheet.\n"
        "5. The lead may only reference the company name and terms present in the company summary (if summary is empty, keep lead generic).\n"
        "6. Output JSON only, no markdown wrappers."
    )

    user_prompt = (
        f"Company Name: {c_name}\n"
        f"Website: {c_site}\n"
        f"Company Type: {c_type}\n"
        f"Company Summary: {c_summary}\n\n"
        f"Candidate Fact Sheet:\n{json.dumps(applicant.FACT_SHEET, indent=2)}\n\n"
        f"Candidate Achievements Bank:\n{json.dumps(applicant.ACHIEVEMENTS, indent=2)}\n"
    )

    try:
        raw_output = _call_llm(provider, model, system_prompt, user_prompt)
        pitch_json = _parse_pitch_json(raw_output)
        errors = validate_pitch(pitch_json, company_row)

        if errors:
            # One retry with errors fed back
            retry_prompt = (
                f"{user_prompt}\n\n"
                f"Your previous output had validation errors:\n"
                + "\n".join(f"- {e}" for e in errors) +
                "\nPlease fix these errors and regenerate the JSON pitch strictly adhering to all rules."
            )
            raw_output = _call_llm(provider, model, system_prompt, retry_prompt)
            pitch_json = _parse_pitch_json(raw_output)
            errors = validate_pitch(pitch_json, company_row)

        if errors:
            fb = fallback_pitch(company_row)
            fb["fallback_reason"] = f"Validation failed after retry: {'; '.join(errors)}"
            fb["provider"] = provider
            fb["model"] = model
            fb["grounded"] = False
            return fb

        # Clean bullets and lead
        pitch_json["lead"] = strip_control_and_html(pitch_json["lead"])
        for b in pitch_json["bullets"]:
            b["title"] = strip_control_and_html(b.get("title", ""))
            b["text"] = strip_control_and_html(b.get("text", ""))

        return {
            "lead": pitch_json["lead"],
            "bullets": pitch_json["bullets"],
            "provider": provider,
            "model": model,
            "grounded": True,
            "fallback_reason": None,
            "generated_at": now_iso()
        }

    except Exception as e:
        fb = fallback_pitch(company_row)
        fb["fallback_reason"] = f"LLM error: {str(e)}"
        fb["provider"] = provider
        fb["model"] = model
        fb["grounded"] = False
        return fb


def ensure_pitch(conn, company_id: int, regenerate: bool = False) -> dict:
    """
    Fetches and stores companies.summary when empty and EXA_API_KEY is configured.
    Caches JSON pitch in companies.pitch via db.update_company.
    Returns the pitch dict.
    """
    company = db.get_company(conn, company_id)
    if not company:
        raise ValueError(f"Company {company_id} not found")

    if not regenerate and company["pitch"]:
        try:
            cached = json.loads(company["pitch"])
            if isinstance(cached, dict) and "lead" in cached and "bullets" in cached:
                return cached
        except Exception:
            pass

    # Check if summary is missing and EXA_API_KEY is configured
    current_summary = company["summary"] or ""
    website = company["website"] or ""
    exa_key = config.get("EXA_API_KEY")

    if not current_summary and exa_key and website:
        try:
            exa = ExaSearch()
            summary_text = exa.company_summary(website)
            if summary_text:
                db.update_company(conn, company_id, summary=summary_text)
                company = db.get_company(conn, company_id)
        except Exception as e:
            print(f"[LLM Tailor] Failed to fetch company summary via Exa: {e}")

    pitch_data = build_pitch(company)
    pitch_json_str = json.dumps(pitch_data)
    db.update_company(conn, company_id, pitch=pitch_json_str)

    return pitch_data
