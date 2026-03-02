"""Shared fixtures — in-memory DB + TestClient."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.db import get_connection, init_db
import app.api as api_module
import app.db as db_module


@pytest.fixture(autouse=True)
def _use_memory_db(tmp_path, monkeypatch):
    """Redirect every test to a fresh in-memory SQLite DB."""
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_db)
    init_db(test_db)
    yield


@pytest.fixture()
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c
