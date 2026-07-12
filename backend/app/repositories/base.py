"""Shared repository helpers for AssetFlow."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generic, Iterator, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Base repository with shared session helpers."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @classmethod
    @contextmanager
    def session_scope(cls, session: Session | None = None) -> Iterator[Session]:
        """Provide a repository-friendly session scope when needed."""

        if session is None:
            from app.database.session import SessionLocal

            db_session = SessionLocal()
            try:
                yield db_session
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise
            finally:
                db_session.close()
            return

        yield session

    def add(self, instance: ModelType) -> ModelType:
        """Persist an ORM instance and flush changes."""

        self.session.add(instance)
        self.session.flush()
        return instance
