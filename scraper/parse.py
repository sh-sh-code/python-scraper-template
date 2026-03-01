"""Parse Hacker News HTML into a list of dicts.

Designed to be resilient — every field except ``title`` is nullable.
If HN changes its markup, individual fields degrade to ``None``
instead of blowing up the whole pipeline.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Optional

from bs4 import BeautifulSoup, Tag

from scraper.logger import setup_logger

log = setup_logger(__name__)

SOURCE = "https://news.ycombinator.com"


def _safe_int(text: Optional[str]) -> Optional[int]:
    """Return the first integer found in *text*, or ``None``."""
    if not text:
        return None
    m = re.search(r"\d+", text)
    return int(m.group()) if m else None


def parse_items(html: str, *, limit: int = 30) -> list[dict[str, Any]]:
    """Parse the HN front-page *html* and return up to *limit* items."""
    soup = BeautifulSoup(html, "html.parser")
    rows: list[Tag] = soup.select("tr.athing")
    items: list[dict[str, Any]] = []

    now = datetime.now(timezone.utc).isoformat()

    for row in rows[:limit]:
        try:
            item = _parse_row(row, now)
            if item is not None:
                items.append(item)
        except Exception:
            log.warning("Skipping unparseable row id=%s", row.get("id"))
            continue

    log.info("Parsed %d / %d rows (limit=%d)", len(items), len(rows), limit)
    return items


def _parse_row(row: Tag, scraped_at: str) -> Optional[dict[str, Any]]:
    """Extract one story from a ``<tr class='athing'>`` and its sibling."""
    item_id_raw = row.get("id")
    if not item_id_raw:
        return None
    item_id = int(item_id_raw)

    # Title & URL
    anchor = row.select_one("td.title .titleline > a") or row.select_one("td.title a")
    title = anchor.get_text(strip=True) if anchor else None
    if not title:
        return None
    url: Optional[str] = anchor.get("href") if anchor else None

    # Rank
    rank_el = row.select_one("span.rank")
    rank = _safe_int(rank_el.get_text()) if rank_el else None

    # Subtext (points, comments)
    subtext = row.find_next_sibling("tr")
    points: Optional[int] = None
    comments_count: Optional[int] = None

    if subtext:
        score_el = subtext.select_one("span.score")
        points = _safe_int(score_el.get_text()) if score_el else None

        for a in subtext.select("a"):
            txt = a.get_text(strip=True).lower()
            if "comment" in txt or "discuss" in txt:
                comments_count = _safe_int(txt)
                break

    return {
        "rank": rank or 0,
        "title": title,
        "url": url,
        "item_id": item_id,
        "points": points,
        "comments_count": comments_count,
        "scraped_at": scraped_at,
        "source": SOURCE,
    }
