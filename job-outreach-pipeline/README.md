# Job Outreach Engine

A direct-outreach pipeline for job hunting: find employers, reach a named decision-maker instead of `info@`,
send a cover letter grounded in your real achievements, follow up in the same email thread, and stop the moment
someone replies or an address bounces.

State lives in a local SQLite database (`outreach.db`, stdlib `sqlite3`, no server). Every send is recorded
atomically together with its RFC 2822 `Message-ID`, so follow-ups thread correctly in Gmail and Outlook.

---

## Architecture

```
 search ──► enrich ──► review ──► generate ──► send ──► check-replies ──► followup
 (Exa)      Hunter      rich TUI    grounded     SMTP      read-only IMAP     In-Reply-To /
            → Prospeo   A/S/E/R/Q   pitch + PDF  + Msg-ID  replies, bounces   References
            → Exa names
              + Hunter finder
            → Apify
                         └──────────────── outreach.db (SQLite) ────────────────┘
```

| File | Purpose |
| :--- | :--- |
| `outreach_pipeline.py` | CLI tying every step together (see commands below). |
| `db.py` | SQLite schema and data access: `companies`, `contacts`, `outreaches`, `inbox_events`. WAL mode, foreign keys, `CHECK` constraints, atomic `record_send`. |
| `migrate_from_csv.py` | One-shot, idempotent import of the old `outreach_queue.csv` / `outreach_log.csv`, with a verification report. |
| `contact_enricher.py` | Decision-maker waterfall: Hunter.io domain search → Prospeo → Exa people search (names and titles) + Hunter Email Finder → Apify scrape fallback. Ranks CTO → VP/Head of Eng → Eng Manager → Head of Talent/HR → Tech Lead → Founder → departmental inbox. Generic inboxes (`info@`, `hello@`) are stored but never made primary. |
| `llm_tailor.py` | Grounded pitch synthesis (Anthropic / OpenAI / Ollama / none) with a code-enforced grounding and style validator. |
| `style_lint.py` | Mechanical-prose checks shared by the validator and the template tests. |
| `triage.py` | Interactive review TUI built on `rich`. |
| `cover_letter_generator.py` | ReportLab PDF letters in IBM Plex Sans. |
| `email_sender.py` | Gmail SMTP client: sets `Message-ID`, `Date`, `List-Unsubscribe`; threads follow-ups with `In-Reply-To` / `References`. |
| `check_inbox.py` | Read-only IMAP scanner: classifies bounces, auto-replies, unsubscribes and replies; backfills Message-IDs of older sends from the Sent folder. |
| `followup_pipeline.py` | Threaded follow-ups 6+ days after the first email, skipping anyone who replied or bounced. |
| `applicant.py` | Your profile, the achievement **fact bank** (`ACHIEVEMENTS`, `FACT_SHEET`), and the first-email and follow-up bodies. |
| `exa_search.py`, `apify_scraper.py`, `config.py` | Exa search + company summaries, Apify contact scraper, `.env` loader. |

### Company lifecycle

`Pending` → (`review`) → `Approved` or `Skipped` → (`send`) → `Sent` / `Failed` → (`followup`) → `Followup-Sent`.
`check-replies` moves any company to `Replied` (reply or unsubscribe request) or `Bounced` (hard bounce); both are
stop states that are never contacted again. `Apply-Online` marks companies that only accept applications through
their careers page.

---

## Setup

1. **Install** (Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure** — `cp .env.example .env` and fill in:
   * `EXA_API_KEY` ([Exa](https://exa.ai)) — employer search and company summaries for grounding.
   * `APIFY_API_TOKEN` ([Apify](https://apify.com)) — website contact scraper (enrichment fallback).
   * `HUNTER_API_KEY`, `PROSPEO_API_KEY` — named decision-makers. Optional: unset or placeholder keys are skipped,
     and the waterfall falls through to Apify.
   * `SENDER_EMAIL`, `GMAIL_APP_PASSWORD` — a Gmail address and a 16-character
     [App Password](https://myaccount.google.com/apppasswords) (needs 2-Step Verification). Used for SMTP and IMAP.
   * `LLM_PROVIDER` (`none` | `anthropic` | `openai` | `ollama`), `LLM_MODEL`, and the matching key or `OLLAMA_HOST`.
     `none` uses the deterministic per-company-type pitch with no network calls.
3. **Profile** — put your CV PDF in this folder and edit `applicant.py` (name, links, `CV_PATH`). Achievements the
   letters may cite live in `applicant.ACHIEVEMENTS`; the LLM can only select and rephrase these.
4. **Database** — new users start empty (`outreach.db` is created on first run). Existing CSV users run
   `python outreach_pipeline.py migrate` once (it backs up any existing DB and verifies counts).

---

## Commands

```bash
python outreach_pipeline.py <command> [options]
```

| Command | What it does |
| :--- | :--- |
| `search "<query>" [local\|remote]` | Exa structured search for employers; adds them as `Pending`. `remote` double-checks that the company's own careers pages accept candidates in Ghana. |
| `enrich [--limit N] [--company NAME] [--refresh] [--dry-run]` | Runs the waterfall for `Pending` companies without a named primary contact (see *Who gets emailed*). Each provider is called at most once per company; quota errors (401/402/429) disable that provider for the rest of the run. A website already scraped is not scraped again unless `--refresh`. |
| `review [--limit N]` | Review TUI. Per company: details, Exa summary, ranked contacts (★ = primary), people found without an email, and the tailored pitch. `[A]`pprove, `[S]`kip, `[E]`dit contact/role (option 4 adds an email for a person found), `[R]`egenerate pitch, `[N]`ext, `[Q]`uit. Approval needs a primary contact that is not a generic inbox; a `careers@`-style inbox needs an explicit yes. |
| `generate` | Compiles cover-letter PDFs for `Approved` companies into `generated_letters/`. |
| `send [--limit 15] [--dry-run]` | Sends the first email (letter + CV) to `Approved` companies, 30–60 s apart, recording each send and its Message-ID in one transaction. Never emails a company twice, and never emails a generic inbox. |
| `check-replies [--days N] [--dry-run] [--test-connection]` | Read-only IMAP scan (`BODY.PEEK`, never marks mail as read). Hard bounces → `Bounced`; replies and unsubscribe requests → `Replied` (with a terminal and desktop alert); out-of-office and delivery *delays* are logged without changing status. Newsletters and your own mail are ignored. |
| `followup [run] [--limit 10]` | Dry-run by default; `run` sends. Checks the inbox first (a live run aborts if IMAP fails), then sends `Re: <original subject>` with `In-Reply-To`/`References` set to the original Message-ID. |
| `migrate [--dry-run]` | Imports the legacy CSVs (idempotent). |
| `status` | Live metrics from `outreach.db`: companies by status, contacts, sends, replies, bounces, follow-ups due. |
| `restart-shared [--dry-run]` | Moves companies whose first email only reached a shared inbox (`info@`, `careers@`) back to `Pending`, so `enrich` can find a named person and `send` can email them. The earlier sends stay as history and their follow-ups stop. A company whose first email reached a person is never emailed cold again. |
| `dump [output.sql]` | Flushes SQLite WAL and exports the database to a version-controllable plain-text SQL script (`outreach_dump.sql`). |

A typical day:
```bash
python outreach_pipeline.py check-replies      # see who answered or bounced
python outreach_pipeline.py enrich --limit 10   # find decision-makers for new companies
python outreach_pipeline.py review              # approve the good ones
python outreach_pipeline.py send --dry-run      # inspect, then:
python outreach_pipeline.py send
python outreach_pipeline.py followup            # dry-run, then: followup run
```

---

## Who gets emailed

Cold outreach goes to a named person: an engineering leader, someone in talent/HR, or a founder. A front-desk
inbox (`info@`, `hello@`, `contact@`) is stored for reference but is never the primary contact and is never
emailed. A hiring inbox (`careers@`, `hr@`, `jobs@`) can be used, but only after you confirm it in `review`.

An address counts as a person only if it reads like a name (`kofi@`, `kofi.mensah@`, `k_mensah@`). Addresses
with digits, the company's own name (`acmetech@gmail.com`) or a role word (`data@`, `team@`) are shared
inboxes; on Gmail/Yahoo/Outlook a single word needs first.last to count.

How named people are found, cheapest first:

1. **Hunter domain search / Prospeo** return people with verified work emails, when the keys are set.
2. **Exa people search** (about $0.007 per company) finds names and titles from LinkedIn, team pages and press,
   with the page that says so. These go into the `people` table and show up in `review`.
3. **Hunter Email Finder** turns the two best-ranked names into addresses. Only a verified address, or one
   with a score of 70+, is kept; addresses are never guessed, because guesses bounce and hurt deliverability.
4. Without a Hunter key, names stay in `review` with their source page; look the person up and add their
   email with `[E]` → 4.

---

## Grounded tailoring

`llm_tailor.ensure_pitch` fetches a company summary (Exa contents API) once, asks the configured LLM for a 1–2
sentence lead plus 2 or 3 bullets selected from `applicant.ACHIEVEMENTS` (two strong matches beat a padded third), and caches the result in
`companies.pitch` so what you approve in `review` is what gets sent. The bullets also replace the generic
highlights in the email body.

The grounding invariant is enforced in code (`validate_pitch`), not just in the prompt:

* every bullet cites an existing `fact_id`, with 2–3 distinct facts;
* every number, metric, technology or proper noun in a bullet **or its title** must appear in that fact's source
  text, so a company's stack can never be claimed as your experience;
* certifications, degrees and employers must appear in `FACT_SHEET`;
* the lead may only name technologies or figures that appear in the company summary, name or domain;
* length caps apply.

The same validator enforces a **human-prose style** (`style_lint.py`). Violations count as errors, so they trigger
the retry like a grounding failure:

* no stock LLM vocabulary (*delve, foster, pivotal, seamless, landscape…*);
* no signpost openers (*Moreover, Furthermore, Ultimately…*);
* at most one em dash per 800 words;
* no editorialising endings (*", highlighting my commitment to…"*);
* no "it's not just X, it's Y" contrasts, hedges or cover-letter clichés (*"I hope this email finds you well"*,
  *"strong interest"*).

Wording from the fact itself is never penalised in its own bullet. The prompt also asks for varied sentence length.
The fixed letter and email templates are held to the same rules, plus a rhythm check (a short sentence somewhere,
no flat cadence, no three sentences in a row opening with the same word). `tests/test_style.py` fails if an edit to
the wording reintroduces any of these.

An invalid pitch gets one retry with the errors fed back. If it fails again, the deterministic per-type pitch is
used and the reason is recorded. Letter generation is never blocked.

---

## Deliverability notes

* **Threading**: every message gets a `Message-ID` that is stored in `outreaches.message_id`. Older sends without
  one are backfilled from Gmail's Sent folder on the first `check-replies` run.
* **Accurate quoting**: the exact body of every email is stored (`outreaches.body`, schema v2). Follow-ups greet the
  contact by name and quote the email the recipient actually received; sends made before v2 aren't quoted, and rely
  on threading instead.
* **Rate limits**: 30–60 s random delay between sends; 15 cold emails and 10 follow-ups per run by default.
* **Stop rules**: `Replied` and `Bounced` companies are excluded by the database query, and `followup run` re-checks
  the inbox immediately before sending.
* **Dry-run first**: `send --dry-run`, `enrich --dry-run`, `check-replies --dry-run` and `followup` (without `run`)
  make no external changes.

---

## Tests

```bash
python -m unittest discover -s tests -t .
```

The suite is hermetic: `tests/__init__.py` blanks every credential, points `OUTREACH_DOTENV` at an empty file and
uses a temporary database, and all SMTP, IMAP and HTTP calls are mocked. Run it from this folder with `-t .` so
that isolation applies.
