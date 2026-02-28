"""Export scraped items to JSON and/or CSV."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from scraper.models import HNItem
from scraper.utils import get_logger

log = get_logger(__name__)

CSV_COLUMNS = [
    "rank",
    "title",
    "url",
    "item_id",
    "points",
    "comments_count",
    "scraped_at",
    "source",
]


def export_json(items: list[HNItem], path: Path) -> Path:
    """Write items to a JSON file and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [item.to_dict() for item in items]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    log.info("Exported %d items → %s", len(items), path)
    return path


def export_csv(items: list[HNItem], path: Path) -> Path:
    """Write items to a CSV file and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for item in items:
            writer.writerow(item.to_dict())
    log.info("Exported %d items → %s", len(items), path)
    return path
