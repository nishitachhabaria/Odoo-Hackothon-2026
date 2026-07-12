"""User repository for authentication workflows."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Department, Role, User
from app.repositories.base import BaseRepository
from app.utils.querying import resolve_sort_expression


class UserRepository(BaseRepository[User]):
    """Repository for user persistence and lookups."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, user_id: UUID) -> User | None:
        """Fetch a user by UUID with role eagerly loaded."""

        statement = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .where(User.id == user_id)
        )
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email with role eagerly loaded."""

        statement = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .where(User.email == email.lower())
        )
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_employee_code(self, employee_code: str) -> User | None:
        """Fetch a user by employee code."""

        statement = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .where(func.lower(User.employee_code) == employee_code.lower())
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

    def list_directory(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        department_id: UUID | None = None,
        role_name: str | None = None,
    ) -> tuple[list[User], int]:
        """Return a paginated employee directory and total count."""

        filters = []
        if search:
            search_term = f"%{search.strip()}%"
            filters.append(
                or_(
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.employee_code.ilike(search_term),
                    Department.name.ilike(search_term),
                    Role.name.ilike(search_term),
                )
            )
        if department_id is not None:
            filters.append(User.department_id == department_id)
        if role_name:
            filters.append(func.lower(Role.name) == role_name.lower())

        total_statement = select(func.count()).select_from(User).join(Role).outerjoin(Department)
        data_statement = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .join(Role)
            .outerjoin(Department)
        )

        if filters:
            total_statement = total_statement.where(*filters)
            data_statement = data_statement.where(*filters)

        sort_expression = resolve_sort_expression(
            sort,
            {
                "first_name": User.first_name,
                "last_name": User.last_name,
                "email": User.email,
                "employee_code": User.employee_code,
                "status": User.status,
                "created_at": User.created_at,
                "updated_at": User.updated_at,
            },
            default_key="created_at",
        )

        data_statement = (
            data_statement.order_by(sort_expression)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        total = int(self.session.execute(total_statement).scalar_one())
        users = list(self.session.execute(data_statement).scalars().all())
        return users, total

    def count_by_department(self, department_id: UUID) -> int:
        """Count employees assigned to a department."""

        statement = select(func.count()).select_from(User).where(User.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def update(self, user: User) -> User:
        """Persist updates to an existing user."""

        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return self.get_by_id(user.id) or user
