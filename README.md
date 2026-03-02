# fastapi-data-api-starter

A production-style REST API built with **FastAPI** and **SQLite**, demonstrating clean architecture, input validation, structured logging, and comprehensive test coverage.

Built as a starter template for freelance backend projects — ready to extend with authentication, PostgreSQL, Docker, or any business logic.

## What This Is

A fully functional CRUD API for managing items (products, resources, records — whatever your domain needs). It's designed to show how I structure real backend projects:

- **FastAPI** for high-performance async routing with auto-generated Swagger docs
- **Pydantic v2** for strict request/response validation
- **SQLite** (stdlib) for zero-config persistence
- **Structured logging** with per-request IDs
- **Proper error handling** (404, 422, 500) with consistent JSON responses
- **Comprehensive tests** using `pytest` + FastAPI `TestClient`

## Quickstart

```bash
git clone https://github.com/sh-sh-code/fastapi-data-api-starter.git
cd fastapi-data-api-starter

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Run the server
uvicorn app.main:app --reload

# Or using Make
make run
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive Swagger UI.

## API Endpoints

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| `GET` | `/health` | Health check | `200` |
| `GET` | `/items` | List items (paginated) | `200` |
| `POST` | `/items` | Create a new item | `201` |
| `GET` | `/items/{id}` | Get item by ID | `200` / `404` |
| `PUT` | `/items/{id}` | Update item (partial) | `200` / `404` |
| `DELETE` | `/items/{id}` | Delete item | `200` / `404` |

## API Examples

### Health check

```bash
curl http://localhost:8000/health
```
```json
{"status": "ok", "version": "1.0.0"}
```

### Create an item

```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Wireless Mouse", "description": "Ergonomic Bluetooth mouse", "price": 29.99, "quantity": 150}'
```
```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "description": "Ergonomic Bluetooth mouse",
  "price": 29.99,
  "quantity": 150,
  "created_at": "2026-03-01 12:00:00",
  "updated_at": "2026-03-01 12:00:00"
}
```

### List items (with pagination)

```bash
curl "http://localhost:8000/items?limit=10&offset=0"
```

### Get a single item

```bash
curl http://localhost:8000/items/1
```

### Update an item (partial)

```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 34.99, "quantity": 200}'
```

### Delete an item

```bash
curl -X DELETE http://localhost:8000/items/1
```
```json
{"detail": "Item deleted"}
```

## Project Structure

```
fastapi-data-api-starter/
├── README.md
├── LICENSE                 # MIT
├── Makefile                # make run / make test
├── requirements.txt
├── .gitignore
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app, middleware, startup
│   ├── api.py              # Route definitions
│   ├── schemas.py          # Pydantic request / response models
│   ├── crud.py             # Database operations
│   ├── db.py               # SQLite connection & schema
│   ├── models.py           # Internal data representations
│   └── logging_config.py   # Logger setup with request IDs
└── tests/
    ├── conftest.py          # Shared fixtures (in-memory DB)
    ├── test_health.py       # Health endpoint tests
    └── test_items.py        # Full CRUD test suite
```

## Running Tests

```bash
pytest -v

# Or using Make
make test
```

## Notes

- **SQLite is intentional** — zero setup, no external services, perfect for demos and small deployments. For production, swap to PostgreSQL by changing `db.py` (or adding SQLAlchemy).
- **No authentication** is included by default. This keeps the template focused on structure and CRUD patterns. Auth can be layered on top (see Extend below).
- **Swagger UI** is available at `/docs` and ReDoc at `/redoc` — great for client demos and testing.
- The logging middleware attaches a unique `request_id` to every request for traceability.

## How to Extend

| Goal | Where to change |
|---|---|
| Add authentication | Add `dependencies` with OAuth2/JWT in `api.py` |
| Switch to PostgreSQL | Replace `db.py` with SQLAlchemy / asyncpg |
| Add Docker | Create `Dockerfile` + `docker-compose.yml` |
| Add CI/CD | Add `.github/workflows/test.yml` with pytest |
| Add more resources | Create new schemas, CRUD functions, and router |
| Background tasks | Add Celery / ARQ workers alongside the API |
| Rate limiting | Add `slowapi` middleware in `main.py` |

## License

[MIT](LICENSE)
