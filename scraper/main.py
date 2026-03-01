"""Pipeline entry-point — fetch → parse → export with proper exit codes.

Usage
-----
    python -m scraper                     # defaults
    python -m scraper --limit 10          # limit items
    python -m scraper --date 2026-03-01   # force a specific date partition
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from scraper.export import export_json
from scraper.fetch import fetch
from scraper.logger import setup_logger
from scraper.parse import parse_items

load_dotenv()

TARGET_URL: str = os.getenv("TARGET_URL", "https://news.ycombinator.com/")
LOG_DIR: str = os.getenv("LOG_DIR", "logs")
DEFAULT_LIMIT: int = int(os.getenv("DEFAULT_LIMIT", "30"))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scraper",
        description="Scrape Hacker News and export to date-partitioned JSON.",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Max items to scrape (default: %(default)s)",
    )
    p.add_argument(
        "--date",
        type=str,
        default=None,
        help="Override date partition (YYYY-MM-DD). Defaults to today.",
    )
    return p


def run(argv: list[str] | None = None) -> int:
    """Execute the full pipeline. Returns 0 on success, 1 on failure."""
    args = build_parser().parse_args(argv)

    run_date = args.date or date.today().isoformat()
    day_dir = Path(LOG_DIR) / run_date

    # Set up logger with file output
    log = setup_logger("scraper", log_file=day_dir / "run.log")

    log.info("=== Pipeline start ===")
    log.info("date=%s  limit=%d  target=%s", run_date, args.limit, TARGET_URL)

    try:
        # 1. Fetch
        html = fetch(TARGET_URL)

        # 2. Parse
        items = parse_items(html, limit=args.limit)
        if not items:
            log.error("No items parsed — aborting")
            return 1

        # 3. Export
        out_path = day_dir / "output.json"
        export_json(items, out_path)

        log.info("=== Pipeline complete — %d items ===", len(items))
        return 0

    except Exception as exc:
        log.exception("Pipeline failed: %s", exc)
        return 1


def main() -> None:
    """CLI wrapper that translates the return code to sys.exit."""
    sys.exit(run())
