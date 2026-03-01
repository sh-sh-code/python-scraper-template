"""HTTP fetching with retry, exponential backoff, timeout, and User-Agent."""

from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv

from scraper.logger import setup_logger

load_dotenv()

log = setup_logger(__name__)

DEFAULT_UA = (
    "Mozilla/5.0 (compatible; ScraperPipeline/1.0; "
    "+https://github.com/sh-sh-code/scraper-scheduler-pipeline)"
)
USER_AGENT: str = os.getenv("USER_AGENT", DEFAULT_UA)
TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))


def fetch(url: str) -> str:
    """Fetch *url* and return the response body as text.

    Retries up to ``MAX_RETRIES`` times with exponential backoff
    (2s, 4s, 8s …) on transient HTTP / connection errors.

    Raises
    ------
    RuntimeError
        If all retry attempts are exhausted.
    """
    headers = {"User-Agent": USER_AGENT}
    last_exc: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info("GET %s (attempt %d/%d)", url, attempt, MAX_RETRIES)
            resp = requests.get(url, headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
            log.info("HTTP %d — %d bytes received", resp.status_code, len(resp.content))
            return resp.text
        except requests.RequestException as exc:
            last_exc = exc
            wait = 2 ** attempt
            log.warning("Attempt %d failed: %s — retrying in %ds", attempt, exc, wait)
            time.sleep(wait)

    raise RuntimeError(
        f"Failed to fetch {url} after {MAX_RETRIES} retries"
    ) from last_exc
