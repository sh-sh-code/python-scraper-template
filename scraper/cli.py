"""CLI entry-point for the scraper."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from scraper.export import export_csv, export_json
from scraper.fetch import fetch
from scraper.parse import parse_items
from scraper.utils import get_logger

load_dotenv()

log = get_logger("scraper")

HN_URL = "https://news.ycombinator.com/"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scraper",
        description="Scrape Hacker News front-page stories.",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=int(os.getenv("DEFAULT_LIMIT", "30")),
        help="Max number of items to scrape (default: 30)",
    )
    p.add_argument(
        "--outdir",
        type=str,
        default=os.getenv("DEFAULT_OUTDIR", "output"),
        help="Output directory (default: output)",
    )
    p.add_argument(
        "--format",
        dest="fmt",
        choices=["json", "csv", "both"],
        default=os.getenv("DEFAULT_FORMAT", "both"),
        help="Output format (default: both)",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    outdir = Path(args.outdir)

    log.info("Starting scrape — limit=%d, format=%s, outdir=%s", args.limit, args.fmt, outdir)

    html = fetch(HN_URL)
    items = parse_items(html, limit=args.limit)

    if not items:
        log.error("No items parsed. Exiting.")
        sys.exit(1)

    if args.fmt in ("json", "both"):
        export_json(items, outdir / "output.json")

    if args.fmt in ("csv", "both"):
        export_csv(items, outdir / "output.csv")

    log.info("Done — %d items scraped.", len(items))
