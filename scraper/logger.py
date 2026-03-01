"""Dual-output logger: stderr (console) + file (date-partitioned)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "scraper",
    log_file: Path | None = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configure and return a logger with console + optional file handlers.

    Parameters
    ----------
    name:      Logger name.
    log_file:  If given, a FileHandler is added that writes to this path.
               Parent directories are created automatically.
    level:     Logging level (default INFO).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers on re-import
    if logger.handlers:
        return logger

    formatter = logging.Formatter(_FMT, datefmt=_DATEFMT)

    # Console → stderr
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File (optional)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
