"""Global exception handlers for AssetFlow."""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def not_found_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Return a clean 404 JSON response."""

    detail = exc.detail if exc.detail else "Resource not found"
    return JSONResponse(status_code=404, content={"detail": detail})


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Return a clean JSON response for HTTP exceptions."""

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return a consistent validation error payload."""

    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Return a generic 500 response and log the original exception."""

    logger.error(
        "Unhandled application error",
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register the platform-level exception handlers."""

    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
