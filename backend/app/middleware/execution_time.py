"""Execution time middleware for AssetFlow."""

from __future__ import annotations

from time import perf_counter

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class ExecutionTimeMiddleware(BaseHTTPMiddleware):
    """Expose request processing time in the response headers."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start = perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time-ms"] = f"{(perf_counter() - start) * 1000:.2f}"
        return response
