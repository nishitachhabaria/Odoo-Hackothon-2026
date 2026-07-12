"""Database initialization helpers."""

from __future__ import annotations

import logging

from sqlalchemy.exc import SQLAlchemyError

from app.database.base import Base
from app.database.session import engine
from app.models import Role, User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

DEFAULT_ROLES: tuple[tuple[str, str], ...] = (
    ("Admin", "Full platform access with role management permissions."),
    ("Employee", "Default employee account for standard access."),
    ("Asset Manager", "Manages assets and allocation workflows."),
    ("Department Head", "Oversees department-level approvals and access."),
)

DEFAULT_ADMIN_EMAIL = "admin@assetflow.com"
DEFAULT_ADMIN_PASSWORD = "Admin@123"


def init_db() -> None:
    """Create database tables for all registered metadata.

    This remains intentionally lightweight so future Alembic migrations can
    take over schema management when domain models are introduced.
    """

    Base.metadata.create_all(bind=engine)

    try:
        with UserRepository.session_scope() as session:
            role_repository = RoleRepository(session)
            user_repository = UserRepository(session)

            for role_name, description in DEFAULT_ROLES:
                role_repository.get_or_create(role_name, description)

            if user_repository.get_by_email(DEFAULT_ADMIN_EMAIL) is None:
                admin_role = role_repository.get_by_name("Admin")
                if admin_role is None:
                    raise RuntimeError("Default Admin role is missing")

                admin_user = User(
                    first_name="System",
                    last_name="Administrator",
                    email=DEFAULT_ADMIN_EMAIL,
                    phone=None,
                    password_hash=get_password_hash(DEFAULT_ADMIN_PASSWORD),
                    department_id=None,
                    role_id=admin_role.id,
                    status="active",
                    is_active=True,
                )
                user_repository.add(admin_user)

    except SQLAlchemyError:
        logger.exception("Unable to seed default roles and admin account")
        raise
