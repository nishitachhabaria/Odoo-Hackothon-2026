"""User repository for authentication workflows."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user persistence and lookups."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, user_id: UUID) -> User | None:
        """Fetch a user by UUID with role eagerly loaded."""

        statement = select(User).options(selectinload(User.role)).where(User.id == user_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email with role eagerly loaded."""

        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email.lower())
        )
        return self.session.execute(statement).scalar_one_or_none()

    def exists_by_email(self, email: str) -> bool:
        """Return whether a user exists for the given email."""

        return self.get_by_email(email) is not None

    def create(self, user: User) -> User:
        """Persist a new user and return the refreshed entity."""

        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return self.get_by_id(user.id) or user
