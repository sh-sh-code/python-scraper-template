"""Shared utilities — logging setup & helpers."""

from __future__ import annotations

import logging
import sys


def get_logger(name: str = "scraper", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger with console handler."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
