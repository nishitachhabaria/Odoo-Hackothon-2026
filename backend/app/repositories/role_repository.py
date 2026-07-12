"""Role repository for RBAC lookups."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for role persistence and lookups."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_name(self, name: str) -> Role | None:
        """Fetch a role by its canonical name."""

        statement = select(Role).where(Role.name == name)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_id(self, role_id: int) -> Role | None:
        """Fetch a role by its primary key."""

        statement = select(Role).where(Role.id == role_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_or_create(self, name: str, description: str | None = None) -> Role:
        """Return an existing role or create a new one."""

        role = self.get_by_name(name)
        if role is not None:
            return role

        role = Role(name=name, description=description)
        self.session.add(role)
        self.session.flush()
        return role
