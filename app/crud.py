"""CRUD operations — pure functions that take a connection + params."""

from __future__ import annotations

import sqlite3
from typing import Any, Optional

from app.logging_config import get_logger

log = get_logger(__name__)


def list_items(
    conn: sqlite3.Connection,
    *,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    cur = conn.execute(
        "SELECT * FROM items ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    )
    return cur.fetchall()


def get_item(conn: sqlite3.Connection, item_id: int) -> Optional[dict[str, Any]]:
    cur = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    return cur.fetchone()


def create_item(
    conn: sqlite3.Connection,
    *,
    name: str,
    description: str = "",
    price: float = 0.0,
    quantity: int = 0,
) -> dict[str, Any]:
    cur = conn.execute(
        """
        INSERT INTO items (name, description, price, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (name, description, price, quantity),
    )
    conn.commit()
    log.info("Created item id=%d", cur.lastrowid)
    return get_item(conn, cur.lastrowid)  # type: ignore[return-value]


def update_item(
    conn: sqlite3.Connection,
    item_id: int,
    **fields: Any,
) -> Optional[dict[str, Any]]:
    existing = get_item(conn, item_id)
    if existing is None:
        return None

    # Only update fields that were explicitly provided
    updates = {k: v for k, v in fields.items() if v is not None}
    if not updates:
        return existing

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values())

    conn.execute(
        f"UPDATE items SET {set_clause}, updated_at = datetime('now') WHERE id = ?",
        [*values, item_id],
    )
    conn.commit()
    log.info("Updated item id=%d fields=%s", item_id, list(updates.keys()))
    return get_item(conn, item_id)


def delete_item(conn: sqlite3.Connection, item_id: int) -> bool:
    cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    if deleted:
        log.info("Deleted item id=%d", item_id)
    return deleted
