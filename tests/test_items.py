"""Tests for /items CRUD endpoints."""

import pytest


SAMPLE_ITEM = {
    "name": "Wireless Mouse",
    "description": "Ergonomic Bluetooth mouse",
    "price": 29.99,
    "quantity": 150,
}


class TestCreateItem:
    def test_create_returns_201(self, client):
        resp = client.post("/items", json=SAMPLE_ITEM)
        assert resp.status_code == 201

    def test_create_returns_all_fields(self, client):
        data = client.post("/items", json=SAMPLE_ITEM).json()
        assert data["name"] == "Wireless Mouse"
        assert data["price"] == 29.99
        assert "id" in data
        assert "created_at" in data

    def test_create_minimal(self, client):
        resp = client.post("/items", json={"name": "Pen"})
        assert resp.status_code == 201
        assert resp.json()["price"] == 0.0

    def test_create_missing_name_returns_422(self, client):
        resp = client.post("/items", json={"price": 10})
        assert resp.status_code == 422

    def test_create_negative_price_returns_422(self, client):
        resp = client.post("/items", json={"name": "X", "price": -1})
        assert resp.status_code == 422


class TestListItems:
    def test_empty_list(self, client):
        resp = client.get("/items")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_after_create(self, client):
        client.post("/items", json=SAMPLE_ITEM)
        client.post("/items", json={"name": "Keyboard", "price": 59.99})
        data = client.get("/items").json()
        assert len(data) == 2

    def test_pagination(self, client):
        for i in range(5):
            client.post("/items", json={"name": f"Item {i}"})
        data = client.get("/items", params={"limit": 2, "offset": 3}).json()
        assert len(data) == 2
        assert data[0]["name"] == "Item 3"


class TestGetItem:
    def test_get_existing(self, client):
        created = client.post("/items", json=SAMPLE_ITEM).json()
        resp = client.get(f"/items/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Wireless Mouse"

    def test_get_nonexistent_returns_404(self, client):
        resp = client.get("/items/9999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Item not found"


class TestUpdateItem:
    def test_partial_update(self, client):
        created = client.post("/items", json=SAMPLE_ITEM).json()
        resp = client.put(
            f"/items/{created['id']}",
            json={"price": 39.99},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["price"] == 39.99
        assert data["name"] == "Wireless Mouse"  # unchanged

    def test_update_nonexistent_returns_404(self, client):
        resp = client.put("/items/9999", json={"name": "Ghost"})
        assert resp.status_code == 404


class TestDeleteItem:
    def test_delete_existing(self, client):
        created = client.post("/items", json=SAMPLE_ITEM).json()
        resp = client.delete(f"/items/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Item deleted"

        # Confirm it's gone
        assert client.get(f"/items/{created['id']}").status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        resp = client.delete("/items/9999")
        assert resp.status_code == 404
