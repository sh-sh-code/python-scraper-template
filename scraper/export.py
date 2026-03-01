"""Export scraped items to a date-partitioned JSON file."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scraper.logger import setup_logger

log = setup_logger(__name__)


def export_json(items: list[dict[str, Any]], path: Path) -> Path:
    """Write *items* as pretty-printed JSON to *path*.

    Parent directories are created automatically.
    Returns the resolved output path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(items, indent=2, ensure_ascii=False) + "\n"
    path.write_text(payload, encoding="utf-8")
    log.info("Exported %d items → %s", len(items), path)
    return path
