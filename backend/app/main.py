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
from app.api.dashboard.router import router as dashboard_router
from app.api.assets.router import router as assets_router
from app.api.asset_categories.router import router as asset_category_router
from app.api.departments.router import router as department_router
from app.api.employees.router import router as employee_router
from app.api.bookings.router import router as bookings_router
from app.database.init_db import init_db
from app.api.auth.router import router as auth_router
from app.middleware import register_middlewares

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""

    logger.info("Starting %s v%s", settings.project_name, settings.version)
    init_db()
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

register_middlewares(app)

register_exception_handlers(app)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(assets_router)
app.include_router(department_router)
app.include_router(asset_category_router)
app.include_router(employee_router)
app.include_router(bookings_router)


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """Return the basic service status payload."""

    return {"message": "AssetFlow API Running"}


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Return a lightweight health response."""

    return {"status": "healthy"}
