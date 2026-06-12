# Empower

**Company intelligence for STEM students recruiting in tech, SWE, data science, and defense.**

Empower is a fusion layer for recruiting. Instead of 10 open tabs that don't talk to each other, you get a single structured signal brief — Claude reads the job descriptions, recent news, compensation data, and company context, and tells you in 30 seconds whether to apply now or keep watching.

Inspired by Palantir's Gotham: ingest from multiple sources, fuse into actionable intelligence, surface what matters.

---

## The problem

Recruiting research is fragmented. During a typical recruiting season you might have Handshake, LinkedIn Jobs, Workday, Indeed, and Greenhouse open simultaneously — lots of data, little clarity. None of it connects.

A student looking at Anduril doesn't need more information. They need something that reads the 12 open JDs, the recent funding news, the Glassdoor comp data, and the Wikipedia founding story, and returns:

> *Series E defense AI company. Aggressively hiring cleared SWEs in Austin and Irvine. L4 comp competitive with FAANG. DoD contract announced in the last 30 days. Strong signal to apply now.*

Empower answers the questions that actually matter: Is this company hiring engineers right now? What seniority and stack? Any clearance requirements? What's changing in the business? What's comp like? Apply now or keep watching?

---

## Features

- **Job board(Future)** — live scraped postings organized by company
- **Signal brief(in progress)** — Claude-fused company brief with a 1–10 score, covering hiring, tech stack, compensation by position, news sentiment
- **Watchlist** — flag companies and get daily re-scores
- **Alerts** — notified on meaningful signal changes: hiring spikes, new roles, funding rounds, sentiment shifts
- **Recruiter discovery(Future)** — public-facing recruiter signals per company

---

## How it works

Every brief fuses four data streams through Claude:

| Source | Signal |
|---|---|
| Job postings (scraped live) | Hiring velocity, seniority distribution, tech stack, clearance requirements |
| News (NewsAPI + RSS) | Funding, layoffs, contracts, sentiment shifts |
| Wikipedia | Company context, ownership, founding story |
| Salary data (Levels.fyi / Glassdoor) | Comp range by level |

Claude acts as the analyst — it reads across all four streams and produces an opinionated brief, not a raw data dump.

In the background, a watcher agent re-runs the fusion daily on flagged companies and fires digest alerts when signals change meaningfully.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Database | PostgreSQL |
| Frontend | React / TypeScript |
| AI | Claude API (Anthropic) |
| Async / scheduling | asyncio, httpx|
| Visualization | D3.js |
| Testing | pytest |

---

## Architecture(Current)

```
backend/
├── services/
│   ├── news.py        ← NewsAPI + RSS fetching
│   ├── wiki.py        ← Wikipedia context
│   ├── salary.py      ← Comp signal fetching
│   ├── claude.py      ← Claude API wrapper
│   └── fusion.py      ← Parallel fetch + brief assembly
├── tests/
│   ├── test_news.py
│   ├── test_wiki.py
│   ├── test_fusion.py
│   ├── test_claude.py
│   └── test_models.py
├── main.py
├── config.py          ← Pydantic settings + env validation
├── cache.py           ← TTL cache (news: 24h, wiki: 7d)
├── models.py
├── .env               ← never committed
├── .env.example       ← committed with placeholder values
├── requirements.txt
└── README.md
```

**Request flow:** Routes → Fusion → Services → Models

Every request flows one direction. Nothing skips a layer. Config loads first and fails loudly if keys are missing or malformed.

**Key decisions:**
- `asyncio` for parallel data fetching — splits latency across all four sources simultaneously
- Pydantic throughout — validates inputs and crashes loud instead of silent failures
- TTL cache — avoids redundant API calls; news resets daily, wiki weekly
- Data provenance on every object — every piece of data carries a source and timestamp

---

## Getting started

**Clone the repo**
```bash
git clone https://github.com/your-username/empower.git
cd empower
```

**Set up the virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Configure environment variables**
```bash
cp .env.example .env
# Fill in your API keys in .env
```

**Run the backend**
```bash
uvicorn main:app --reload
```

**Run tests**
```bash
pytest
```

---

## Environment variables

```
ANTHROPIC_API_KEY=
NEWS_API_KEY=
```

Never commit `.env`. The `.env.example` file contains placeholder values for reference.

---

## Roadmap

- [x] News + Wikipedia fusion via Claude
- [x] Validated architecture with parallel async fetching
- [x] TTL caching layer with data provenance
- [ ] Job board (live scraped postings)
- [ ] Full signal brief with 1–10 score (in progress)
- [ ] Flagged company watchlist with daily re-score
- [ ] Digest alerts on signal changes
- [ ] Recruiter discovery

---

## Security notes

- All API keys loaded from environment, never committed
- Input validation via Pydantic — `company_name` enforces `min_length=1, max_length=100`
- Rate limiting via `slowapi` to prevent API quota drain
- Errors are caught and returned as clean messages — raw exceptions are never surfaced to the client
- Deployed over HTTPS

---

No rights reserved lol, let me know how I can improve this project!
