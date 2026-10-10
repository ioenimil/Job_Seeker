# 🚀 Automated Cold Job Outreach & Follow-up Pipeline

An end-to-end automated cold job application and follow-up engine designed to execute high-volume, personalized outreach campaigns. By leveraging semantic web search, contact details harvesting, verified B2B email search, and automated email threading, this codebase turns cold job hunting into an autonomous pipeline.

It is structured so that **any human user or AI coding agent** can clone the repository, add their credentials and CV, and manage their job application campaign.

---

## 🛠️ Architecture Overview

The pipeline consists of three core phases that can be run manually or triggered autonomously by an AI agent:

```
[Phase 1: DISCOVER] ──> [Phase 2: ENRICH] ──> [Phase 3: SEND & FOLLOW-UP]
  - Exa.ai Search          - Hunter.io API         - ReportLab PDF Letter Compiler
  - Directory Imports      - Prospeo API           - Secure SMTP SSL Client
                           - LinkedIn Matching     - Automated Follow-up Threading
```

*   **Phase 1: Discover:** Find companies based on custom search queries (e.g., target location, industry, funding stage, tech stack) using semantic web search, or import static target lists.
*   **Phase 2: Enrich:** Scrape domain contacts, identify key technical decision-makers (CTOs, Engineering Managers, HR heads) on LinkedIn, and retrieve their direct corporate emails.
*   **Phase 3: Send & Follow-up:** Dynamic-compile personalized cover letter PDFs tailored to the company's profile, attach your master CV, send via Gmail SMTP with anti-spam delays, and execute automatic in-thread follow-up check-ins 6 days later.

---

## 📂 Repository Structure

| File | Purpose |
| :--- | :--- |
| **`outreach_pipeline.py`** | Main orchestrator to run search, scrape, letter generation, and cold sends. |
| **`followup_pipeline.py`** | Follow-up manager to check candidate dates, apply exclusions, and send in-thread check-ins. |
| **`email_sender.py`** | Secure SMTP client with attachment routing. |
| **`cover_letter_generator.py`** | Dynamic PDF compiler using ReportLab styles. |
| **`applicant.py`** | Your profile: name, contact links, headline, CV path, target roles, and cold email body. |
| **`config.py`** | Zero-dependency environment variable loader. |
| **`apify_scraper.py`** | Apify Actor interface for crawling domain contact pages. |
| **`exa_search.py`** | Exa API wrapper for semantic queries. |
| **`outreach_queue.csv`** | Central SQLite-like tracking database of target companies and statuses. `scope`, `ghana_eligibility`, `evidence_url` and `careers_url` record why each company qualifies and where to apply. |
| **`outreach_log.csv`** | History of successfully executed sends and timestamps. |

---

## 🚀 Setup Instructions

Follow these steps to get your own job outreach campaign running:

### 1. Clone & Install Dependencies
Clone this repository to your machine. Make sure you have Python 3.10+ installed. Install the required libraries:
```bash
pip install requests reportlab
```

### 2. Configure Credentials
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and fill in your details:
*   **`EXA_API_KEY`:** Get a key from [Exa.ai](https://exa.ai) (1000 free searches/month).
*   **`APIFY_API_TOKEN`:** Get a token from [Apify](https://apify.com) to run the contact scraper.
*   **`HUNTER_API_KEY`** & **`PROSPEO_API_KEY`:** (Optional but highly recommended) Accounts with Hunter.io and Prospeo.io to verify direct email addresses of decision-makers.
*   **`SENDER_EMAIL`:** Your Gmail address.
*   **`GMAIL_APP_PASSWORD`:** A 16-character Google App Password (not your normal password). You must have 2-Step Verification enabled to create this at [Google App Passwords](https://myaccount.google.com/apppasswords).

### 3. Add Your CV & Profile
1. Save your master resume as a PDF in the `job-outreach-pipeline/` directory.
2. Open `applicant.py` and set your name, contact details, headline, and `CV_PATH` to match your resume's filename:
   ```python
   CV_PATH = "Your_Name_CV.pdf"
   ```
3. Cover letter wording per `company_type` lives in `cover_letter_generator.py`; the cold email body lives in `applicant.py`.

Supported `company_type` values: `general_startup`, `consultancy`, `fintech`, `isp`/`telecom`, `bank`, and `ai`. AI/ML companies (`ai`) are pitched for a Forward Deployed Engineer role. Consultancies get a Forward Deployed / Platform Engineer pitch. Every other type is pitched for a Platform & DevOps Engineer role (see `ROLE_BY_TYPE` in `applicant.py`).

### 4. Create the Target Queue
Copy the database template to start fresh:
```bash
cp outreach_queue.example.csv outreach_queue.csv
```

---

## 💻 CLI Commands

Run the orchestrator using Python:

| Command | Usage | Description |
| :--- | :--- | :--- |
| **Search** | `py outreach_pipeline.py search "[query]" [local\|remote]` | Find employers with Exa structured search. `local` (default) keeps companies based in Ghana; `remote` keeps remote companies whose own careers pages show Ghana is an eligible hiring location (each one is double-checked, and US/EU-only firms are skipped). E.g. `py outreach_pipeline.py search "remote-first startups hiring engineers in Africa" remote` |
| **Scrape** | `py outreach_pipeline.py scrape` | Crawls target homepages to resolve domains and identify general emails. |
| **Generate** | `py outreach_pipeline.py generate` | Dynamic-compiles cover letter PDFs inside `generated_letters/` for inspection. |
| **Send** | `py outreach_pipeline.py send` | Sends emails to up to 15 companies marked as `Approved` in `outreach_queue.csv` and marks them `Sent`. |
| **Status** | `py outreach_pipeline.py status` | Outputs current counts of the queue (Pending, Approved, Sent, Skipped). |

### 🔁 Running Follow-ups
To check for and send professional follow-ups:

*   **Dry-run (Review Candidates):**
    ```bash
    py followup_pipeline.py
    ```
    Displays which targets sent 6+ days ago are eligible for a follow-up and what text they will receive.
*   **Live Send (Up to 10):**
    ```bash
    py followup_pipeline.py run
    ```
    Executes the follow-up check-ins and marks the status as `Followup-Sent` in the database.

---

## 🤖 AI Agent Delegation (How to let an AI run this)

This repository is optimized for autonomous execution by AI agents (e.g. Cursor, Claude Code, Gemini Agent). You can instruct the agent with simple tasks:

*   **To find leads:** *"Agent, search for 15 remote-friendly Cloud companies hiring in Africa, enrich their contact details, and save them to the queue."*
*   **To verify & approve:** *"Agent, open outreach_queue.csv, check the scraped emails, clean up duplicates, and mark the high-value targets as Approved."*
*   **To execute cold sends:** *"Agent, compile the cover letters, check SMTP settings, and run the pipeline to send the daily batch."*
*   **To run check-ins:** *"Agent, look for any outreaches sent at least 6 days ago and run the follow-up pipeline to send them a polite status update."*
*   **To read replies:** *"Agent, run check_emails.py to pull new messages from my inbox, summarize response threads, and help me draft replies to active leads."*

---

## ⚠️ Safeguards & Rate Limits
*   **Spam Controls:** The script enforces a **30-60 second random delay** between emails to bypass spam triggers.
*   **Daily Caps:** Cold outreach is capped at **15 emails per day** by default, and follow-ups are capped at **10 per day** to protect your domain reputation.
*   **Review Queue:** You can inspect all draft layouts in `generated_letters/` prior to running the send scripts.
