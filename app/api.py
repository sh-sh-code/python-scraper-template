"""API route definitions — all /items endpoints + /health."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app import crud
from app.db import get_connection
from app.logging_config import get_logger
from app.schemas import (
    HealthResponse,
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    MessageResponse,
)

log = get_logger(__name__)

router = APIRouter()

APP_VERSION = "1.0.0"


# ──────────────────────────── Health ────────────────────────────

@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    response_model=HealthResponse,
)
def health_check() -> HealthResponse:
    """Return service status. Use this for uptime monitoring."""
    return HealthResponse(status="ok", version=APP_VERSION)


# ──────────────────────────── Items ─────────────────────────────

@router.get(
    "/items",
    tags=["Items"],
    summary="List items",
    response_model=list[ItemResponse],
)
def list_items(
    limit: int = Query(100, ge=1, le=1000, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
) -> list[ItemResponse]:
    """Retrieve a paginated list of items."""
    conn = get_connection()
    try:
        rows = crud.list_items(conn, limit=limit, offset=offset)
        return [ItemResponse(**r) for r in rows]
    finally:
        conn.close()


@router.post(
    "/items",
    tags=["Items"],
    summary="Create an item",
    response_model=ItemResponse,
    status_code=201,
)
def create_item(body: ItemCreate) -> ItemResponse:
    """Create a new item and return it."""
    conn = get_connection()
    try:
        row = crud.create_item(
            conn,
            name=body.name,
            description=body.description,
            price=body.price,
            quantity=body.quantity,
        )
        return ItemResponse(**row)
    finally:
        conn.close()


@router.get(
    "/items/{item_id}",
    tags=["Items"],
    summary="Get an item by ID",
    response_model=ItemResponse,
)
def get_item(item_id: int) -> ItemResponse:
    """Retrieve a single item. Returns 404 if not found."""
    conn = get_connection()
    try:
        row = crud.get_item(conn, item_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemResponse(**row)
    finally:
        conn.close()


@router.put(
    "/items/{item_id}",
    tags=["Items"],
    summary="Update an item",
    response_model=ItemResponse,
)
def update_item(item_id: int, body: ItemUpdate) -> ItemResponse:
    """Update an existing item (partial update). Returns 404 if not found."""
    conn = get_connection()
    try:
        row = crud.update_item(
            conn,
            item_id,
            name=body.name,
            description=body.description,
            price=body.price,
            quantity=body.quantity,
        )
        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemResponse(**row)
    finally:
        conn.close()


@router.delete(
    "/items/{item_id}",
    tags=["Items"],
    summary="Delete an item",
    response_model=MessageResponse,
)
def delete_item(item_id: int) -> MessageResponse:
    """Delete an item by ID. Returns 404 if not found."""
    conn = get_connection()
    try:
        if not crud.delete_item(conn, item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        return MessageResponse(detail="Item deleted")
    finally:
        conn.close()
