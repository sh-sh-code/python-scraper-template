"""Data models for scraped items."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class HNItem:
    """A single Hacker News front-page story."""

    title: str
    url: Optional[str]
    rank: int
    item_id: int
    points: Optional[int] = None
    comments_count: Optional[int] = None
    scraped_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "https://news.ycombinator.com"

    def to_dict(self) -> dict:
        return asdict(self)
