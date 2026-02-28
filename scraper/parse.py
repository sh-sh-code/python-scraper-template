"""Parse Hacker News HTML into structured items."""

from __future__ import annotations

import re
from typing import Optional

from bs4 import BeautifulSoup, Tag

from scraper.models import HNItem
from scraper.utils import get_logger

log = get_logger(__name__)


def _safe_int(text: Optional[str]) -> Optional[int]:
    """Extract the first integer from *text*, or return None."""
    if not text:
        return None
    m = re.search(r"\d+", text)
    return int(m.group()) if m else None


def parse_items(html: str, *, limit: int = 30) -> list[HNItem]:
    """Parse the HN front page HTML and return up to *limit* items."""
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr.athing")
    items: list[HNItem] = []

    for row in rows[:limit]:
        try:
            item = _parse_row(row)
            if item:
                items.append(item)
        except Exception:
            log.warning("Skipping unparseable row id=%s", row.get("id"))
            continue

    log.info("Parsed %d items (limit=%d)", len(items), limit)
    return items


def _parse_row(row: Tag) -> Optional[HNItem]:
    """Parse a single <tr class='athing'> and its sibling subtext row."""
    item_id_str = row.get("id")
    if not item_id_str:
        return None
    item_id = int(item_id_str)

    # --- Title & URL ---
    title_anchor = row.select_one("td.title .titleline > a")
    if title_anchor is None:
        title_anchor = row.select_one("td.title a")
    title = title_anchor.get_text(strip=True) if title_anchor else None
    if not title:
        return None
    url = title_anchor.get("href") if title_anchor else None

    # --- Rank ---
    rank_el = row.select_one("span.rank")
    rank = _safe_int(rank_el.get_text()) if rank_el else None

    # --- Subtext row (points, comments) ---
    subtext = row.find_next_sibling("tr")
    points: Optional[int] = None
    comments_count: Optional[int] = None

    if subtext:
        score_el = subtext.select_one("span.score")
        points = _safe_int(score_el.get_text()) if score_el else None

        for a_tag in subtext.select("a"):
            txt = a_tag.get_text(strip=True).lower()
            if "comment" in txt or "discuss" in txt:
                comments_count = _safe_int(txt)
                break

    return HNItem(
        title=title,
        url=url,
        rank=rank or 0,
        item_id=item_id,
        points=points,
        comments_count=comments_count,
    )
