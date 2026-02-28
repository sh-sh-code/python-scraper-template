# python-scraper-template

A production-ready Python web scraper template that collects front-page stories from [Hacker News](https://news.ycombinator.com/).
Built as a reusable starting point for freelance scraping projects.

## What It Does

- Scrapes the Hacker News front page and extracts structured data per story:
  - `title`, `url`, `rank`, `item_id`, `points`, `comments_count`, `scraped_at`, `source`
- Exports results in **JSON** and/or **CSV** format
- Production-grade practices out of the box:
  - Automatic retry with exponential backoff
  - Configurable request timeout & User-Agent
  - Structured logging to stderr
  - Null-safe parsing (gracefully handles missing fields)

## Quick Start

```bash
# Clone
git clone https://github.com/sh-sh-code/python-scraper-template.git
cd python-scraper-template

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) copy .env
cp .env.example .env

# Run
python -m scraper --limit 30 --outdir output --format both
```

## CLI Options

```
usage: scraper [-h] [--limit LIMIT] [--outdir OUTDIR] [--format {json,csv,both}]

options:
  --limit   Max number of items to scrape (default: 30)
  --outdir  Output directory (default: output)
  --format  Output format: json | csv | both (default: both)
```

### Examples

```bash
# Scrape top 10 stories, JSON only
python -m scraper --limit 10 --format json

# Scrape 30 stories to a custom directory
python -m scraper --outdir data/2026-02

# CSV only
python -m scraper --format csv
```

## Output

### JSON (`output/output.json`)

```json
[
  {
    "title": "Show HN: A open-source tool for generating UIs with AI",
    "url": "https://github.com/example/project",
    "rank": 1,
    "item_id": 39012345,
    "points": 284,
    "comments_count": 93,
    "scraped_at": "2026-02-28T12:00:00+00:00",
    "source": "https://news.ycombinator.com"
  }
]
```

### CSV (`output/output.csv`)

```
rank,title,url,item_id,points,comments_count,scraped_at,source
1,Show HN: A open-source tool for generating UIs with AI,https://github.com/example/project,39012345,284,93,2026-02-28T12:00:00+00:00,https://news.ycombinator.com
```

## Project Structure

```
python-scraper-template/
├── README.md
├── LICENSE                # MIT
├── pyproject.toml         # Package metadata & dependencies
├── requirements.txt       # Pinned dependencies
├── .gitignore
├── .env.example           # Environment variable template
├── scraper/
│   ├── __init__.py
│   ├── __main__.py        # python -m scraper entry point
│   ├── cli.py             # Argument parsing & orchestration
│   ├── fetch.py           # HTTP fetching (retry, backoff, timeout)
│   ├── parse.py           # HTML → structured data
│   ├── export.py          # JSON & CSV export
│   ├── models.py          # Dataclass definitions
│   └── utils.py           # Logging setup
├── examples/
│   ├── sample_output.json
│   └── sample_output.csv
└── tests/
    ├── test_parse.py      # Parser unit tests
    └── test_export.py     # Exporter unit tests
```

## Running Tests

```bash
pip install -r requirements.txt
pytest
```

## Notes

- This scraper targets the **publicly accessible** Hacker News front page only.
- Requests include a descriptive `User-Agent` header identifying the bot.
- HN does not require authentication for its front page; no API key is needed.
- Fields like `points` and `comments_count` are optional — if HN's markup changes, the scraper returns `null` instead of crashing.

## How to Extend

| Goal | Where to change |
|---|---|
| Scrape a different site | Update `cli.py` (URL) + rewrite `parse.py` |
| Add more fields | Extend `HNItem` in `models.py`, update `parse.py` and `CSV_COLUMNS` in `export.py` |
| Save to a database | Add a new exporter in `export.py` (e.g. `export_sqlite`) |
| Schedule periodic runs | Wrap with `cron`, Airflow, or a GitHub Actions workflow |
| Add pagination | Loop in `cli.py`, passing `?p=2`, `?p=3` … to `fetch()` |

## License

[MIT](LICENSE)
