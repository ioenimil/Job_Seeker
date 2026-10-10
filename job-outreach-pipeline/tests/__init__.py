# Keep the suite hermetic: never read the real .env (API keys, Gmail password) or touch outreach.db.
# Run from job-outreach-pipeline/ with:  python -m unittest discover -s tests -t .
import os
import tempfile

os.environ["OUTREACH_DOTENV"] = os.devnull
os.environ["OUTREACH_DB"] = os.path.join(tempfile.mkdtemp(prefix="outreach-test-"), "outreach.db")
for key in ("APIFY_API_TOKEN", "EXA_API_KEY", "HUNTER_API_KEY", "PROSPEO_API_KEY", "SENDER_EMAIL",
            "GMAIL_APP_PASSWORD", "LLM_PROVIDER", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    os.environ.pop(key, None)
