"""Pydantic schemas — request / response validation."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ---------- Request bodies ----------

class ItemCreate(BaseModel):
    """Body for POST /items."""

    name: str = Field(..., min_length=1, max_length=200, examples=["Wireless Mouse"])
    description: str = Field("", max_length=1000, examples=["Ergonomic Bluetooth mouse"])
    price: float = Field(0.0, ge=0, examples=[29.99])
    quantity: int = Field(0, ge=0, examples=[150])


class ItemUpdate(BaseModel):
    """Body for PUT /items/{id}.  All fields optional for partial update."""

    name: Optional[str] = Field(None, min_length=1, max_length=200, examples=["Wireless Mouse v2"])
    description: Optional[str] = Field(None, max_length=1000, examples=["Updated description"])
    price: Optional[float] = Field(None, ge=0, examples=[34.99])
    quantity: Optional[int] = Field(None, ge=0, examples=[200])


# ---------- Response bodies ----------

class ItemResponse(BaseModel):
    """Single item returned from the API."""

    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Wireless Mouse"])
    description: str = Field(..., examples=["Ergonomic Bluetooth mouse"])
    price: float = Field(..., examples=[29.99])
    quantity: int = Field(..., examples=[150])
    created_at: str = Field(..., examples=["2026-03-01 12:00:00"])
    updated_at: str = Field(..., examples=["2026-03-01 12:00:00"])


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    version: str = Field(..., examples=["1.0.0"])


class MessageResponse(BaseModel):
    detail: str = Field(..., examples=["Item deleted"])
