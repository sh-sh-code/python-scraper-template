"""FastAPI application factory and middleware."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router
from app.db import init_db
from app.logging_config import generate_request_id, get_logger, setup_logging

setup_logging()
log = get_logger(__name__)


# ────────────────────── Lifespan ───────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    log.info("Application started")
    yield
    log.info("Application shutdown")


app = FastAPI(
    title="FastAPI Data API Starter",
    description=(
        "A lightweight REST API starter built with FastAPI and SQLite. "
        "Demonstrates clean project structure, validation, error handling, "
        "and Swagger documentation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ───────────────── Middleware: request logging ──────────────────

@app.middleware("http")
async def request_logging(request: Request, call_next):
    request_id = generate_request_id()
    log.info(
        "[%s] %s %s",
        request_id,
        request.method,
        request.url.path,
    )
    response = await call_next(request)
    log.info("[%s] → %d", request_id, response.status_code)
    return response


# ────────────────── Global exception handler ───────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ──────────────────────── Routes ───────────────────────────────

app.include_router(router)
