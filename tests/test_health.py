"""Tests for GET /health."""


class TestHealth:
    def test_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_body_shape(self, client):
        data = client.get("/health").json()
        assert data["status"] == "ok"
        assert "version" in data
