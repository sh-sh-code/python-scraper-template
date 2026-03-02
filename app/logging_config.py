"""Structured logging with request-id support."""

from __future__ import annotations

import logging
import os
import sys
import uuid

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """Configure the root logger once."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=_FMT,
        datefmt=_DATEFMT,
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def generate_request_id() -> str:
    return uuid.uuid4().hex[:12]
