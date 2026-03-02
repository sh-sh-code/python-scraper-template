"""SQLite connection helper using the stdlib sqlite3 module.

Keeps things simple: one file-based DB, WAL mode for concurrency,
and a straightforward dict-row factory.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from app.logging_config import get_logger

load_dotenv()

log = get_logger(__name__)

_DB_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")
# Strip the "sqlite:///" prefix to get the file path
DB_PATH = _DB_URL.replace("sqlite:///", "")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    description TEXT   NOT NULL DEFAULT '',
    price      REAL    NOT NULL DEFAULT 0.0,
    quantity   INTEGER NOT NULL DEFAULT 0,
    created_at TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""


def _dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    """Row factory that returns dicts instead of tuples."""
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    """Return a new connection with WAL mode and dict rows."""
    path = db_path if db_path is not None else DB_PATH
    conn = sqlite3.Connection(path)
    conn.row_factory = _dict_factory
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str | None = None) -> None:
    """Create tables if they don't exist."""
    path = db_path if db_path is not None else DB_PATH
    conn = get_connection(path)
    try:
        conn.executescript(_SCHEMA)
        log.info("Database initialized: %s", path)
    finally:
        conn.close()
