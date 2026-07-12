"""Middleware package exports for AssetFlow."""

from fastapi import FastAPI

from app.middleware.execution_timer import ExecutionTimeMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_middlewares(app: FastAPI) -> None:
	"""Register all application middleware in one place."""

	app.add_middleware(RequestLoggingMiddleware)
	app.add_middleware(ExecutionTimeMiddleware)
	app.add_middleware(SecurityHeadersMiddleware)


