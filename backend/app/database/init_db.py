"""Database initialization helpers."""

from __future__ import annotations

from app.database.base import Base
from app.database.session import engine


def init_db() -> None:
    """Create database tables for all registered metadata.

    This remains intentionally lightweight so future Alembic migrations can
    take over schema management when domain models are introduced.
    """

    Base.metadata.create_all(bind=engine)
