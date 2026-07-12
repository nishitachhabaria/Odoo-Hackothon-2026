"""AssetFlow FastAPI application entrypoint.

This module wires the platform foundation only. Business modules, CRUD
routers, and domain workflows are intentionally excluded for now.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.database.init_db import init_db
from app.api.auth.router import router as auth_router
from app.middleware.execution_time import ExecutionTimeMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""

    logger.info("Starting %s v%s", settings.project_name, settings.version)
    try:
        init_db()
    except Exception:  # pragma: no cover - startup safety net
        logger.exception("AssetFlow database initialization skipped due to an error")
    yield
    logger.info("Shutting down %s", settings.project_name)


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=(
        "AssetFlow is an enterprise asset and resource management platform "
        "foundation built with FastAPI, PostgreSQL, and SQLAlchemy."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ExecutionTimeMiddleware)

register_exception_handlers(app)
app.include_router(auth_router)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Return the basic service status payload."""

    return {"message": "AssetFlow API Running"}


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return a lightweight health response."""

    return {"status": "healthy"}
