"""Internal data representations (thin wrapper around DB rows).

For a project this size the Pydantic schemas in schemas.py double as
the "model" layer.  This module exists to keep the door open for
richer domain logic without polluting the API schemas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    id: int
    name: str
    description: str
    price: float
    quantity: int
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: dict) -> "Item":
        return cls(**row)
