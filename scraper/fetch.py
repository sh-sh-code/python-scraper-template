"""HTTP fetching with retry / backoff / timeout / User-Agent."""

from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv

from scraper.utils import get_logger

load_dotenv()

log = get_logger(__name__)

DEFAULT_UA = (
    "Mozilla/5.0 (compatible; PythonScraperTemplate/0.1; "
    "+https://github.com/sh-sh-code/python-scraper-template)"
)
USER_AGENT = os.getenv("USER_AGENT", DEFAULT_UA)
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))


def fetch(url: str) -> str:
    """Fetch *url* and return the response text.

    Retries on transient errors with exponential backoff.
    """
    headers = {"User-Agent": USER_AGENT}
    last_exc: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info("GET %s (attempt %d/%d)", url, attempt, MAX_RETRIES)
            resp = requests.get(url, headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
            log.info("OK %d — %d bytes", resp.status_code, len(resp.content))
            return resp.text
        except requests.RequestException as exc:
            last_exc = exc
            wait = 2 ** attempt
            log.warning("Attempt %d failed: %s — retrying in %ds", attempt, exc, wait)
            time.sleep(wait)

    raise RuntimeError(
        f"Failed to fetch {url} after {MAX_RETRIES} attempts"
    ) from last_exc
