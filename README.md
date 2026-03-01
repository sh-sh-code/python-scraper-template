# scraper-scheduler-pipeline

A **cron-ready** web scraper pipeline that collects Hacker News front-page stories and writes date-partitioned JSON output with structured logging.

Built to demonstrate **production-grade scraping practices**: retry with backoff, proper exit codes, per-run log files, and zero manual intervention during scheduled execution.

## Features

| Capability | Detail |
|---|---|
| Target | [Hacker News](https://news.ycombinator.com/) front page |
| Output | `logs/YYYY-MM-DD/output.json` |
| Run log | `logs/YYYY-MM-DD/run.log` |
| Retry | Exponential backoff (2 s → 4 s → 8 s) |
| Timeout | Configurable per-request timeout |
| User-Agent | Descriptive, configurable via `.env` |
| Exit codes | `0` = success, `1` = failure |
| Scheduling | Shell wrappers for cron / launchd |

## Quick Start

```bash
git clone https://github.com/sh-sh-code/scraper-scheduler-pipeline.git
cd scraper-scheduler-pipeline

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

python -m scraper --limit 30
```

## CLI Options

```
usage: scraper [-h] [--limit LIMIT] [--date DATE]

options:
  --limit  Max items to scrape (default: 30)
  --date   Override date partition, YYYY-MM-DD (default: today)
```

### Examples

```bash
# Default — scrape 30 items, today's date
python -m scraper

# Limit to 10
python -m scraper --limit 10

# Backfill a specific date
python -m scraper --date 2026-02-28

# Via shell wrapper
./scripts/run_once.sh --limit 20
```

## Output Structure

After a successful run on `2026-03-01`:

```
logs/
└── 2026-03-01/
    ├── output.json    ← scraped data
    └── run.log        ← execution log
```

### Sample JSON (`logs/2026-03-01/output.json`)

```json
[
  {
    "rank": 1,
    "title": "Show HN: An open-source AI code editor",
    "url": "https://github.com/example/editor",
    "item_id": 41000001,
    "points": 312,
    "comments_count": 127,
    "scraped_at": "2026-03-01T06:00:00+00:00",
    "source": "https://news.ycombinator.com"
  }
]
```

### Sample Log (`logs/2026-03-01/run.log`)

```
2026-03-01 06:00:00 [INFO] scraper: === Pipeline start ===
2026-03-01 06:00:00 [INFO] scraper: date=2026-03-01  limit=30  target=https://news.ycombinator.com/
2026-03-01 06:00:00 [INFO] scraper.fetch: GET https://news.ycombinator.com/ (attempt 1/3)
2026-03-01 06:00:01 [INFO] scraper.fetch: HTTP 200 — 43210 bytes received
2026-03-01 06:00:01 [INFO] scraper.parse: Parsed 30 / 30 rows (limit=30)
2026-03-01 06:00:01 [INFO] scraper.export: Exported 30 items → logs/2026-03-01/output.json
2026-03-01 06:00:01 [INFO] scraper: === Pipeline complete — 30 items ===
```

## Scheduling with cron

### Daily at 06:00 (system timezone)

```cron
0 6 * * * /home/you/scraper-scheduler-pipeline/scripts/run_daily.sh >> /tmp/scraper-cron.log 2>&1
```

### Every 6 hours

```cron
0 */6 * * * /home/you/scraper-scheduler-pipeline/scripts/run_daily.sh >> /tmp/scraper-cron.log 2>&1
```

### macOS launchd (alternative)

Create `~/Library/LaunchAgents/com.scraper.daily.plist` and load with `launchctl`.

## Project Structure

```
scraper-scheduler-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── scraper/
│   ├── __init__.py
│   ├── __main__.py       # python -m scraper entry point
│   ├── main.py           # Pipeline orchestration + exit codes
│   ├── fetch.py          # HTTP fetch with retry & backoff
│   ├── parse.py          # HTML → dict (null-safe)
│   ├── export.py         # JSON export
│   └── logger.py         # Dual-output logger (stderr + file)
├── scripts/
│   ├── run_once.sh       # One-shot wrapper
│   └── run_daily.sh      # Cron wrapper with date handling
├── examples/
│   └── sample_output.json
├── logs/                  # Created at runtime (git-ignored)
│   └── .gitkeep
└── tests/
    └── test_parse.py
```

## Running Tests

```bash
pytest -v
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TARGET_URL` | `https://news.ycombinator.com/` | Page to scrape |
| `REQUEST_TIMEOUT` | `10` | HTTP timeout in seconds |
| `MAX_RETRIES` | `3` | Retry attempts on failure |
| `USER_AGENT` | *(built-in)* | Custom User-Agent string |
| `LOG_DIR` | `logs` | Base directory for output & logs |
| `DEFAULT_LIMIT` | `30` | Default item limit |

## Error Handling

| Scenario | Behavior |
|---|---|
| Network timeout | Retry with exponential backoff (up to 3 attempts) |
| HTTP 4xx / 5xx | Retry, then exit 1 |
| Parse yields 0 items | Exit 1 with error log |
| Unexpected exception | Logged with traceback, exit 1 |
| Success | Exit 0 |

## How to Extend

| Goal | Where to change |
|---|---|
| Different target site | Set `TARGET_URL` in `.env`, rewrite `parse.py` |
| Add CSV/DB export | Add a function in `export.py`, call it from `main.py` |
| Pagination | Loop in `main.py` with `?p=2`, `?p=3`, … |
| Alerting on failure | Check exit code in `run_daily.sh`, send Slack/email |
| Docker | Add a `Dockerfile` + `docker-compose.yml` |

## License

MIT
