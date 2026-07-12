"""Department repository for organization setup data access."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Department, User
from app.repositories.base import BaseRepository
from app.utils.querying import resolve_sort_expression


class DepartmentRepository(BaseRepository[Department]):
    """Repository for department persistence and search queries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, department_id: UUID) -> Department | None:
        """Return a department by UUID."""

        statement = select(Department).where(Department.id == department_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_name(self, name: str) -> Department | None:
        """Return a department by unique name."""

        statement = select(Department).where(func.lower(Department.name) == name.lower())
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_code(self, code: str) -> Department | None:
        """Return a department by unique code."""

        statement = select(Department).where(func.lower(Department.code) == code.lower())
        return self.session.execute(statement).scalar_one_or_none()

    def exists_by_name(self, name: str) -> bool:
        """Check whether a department name is already in use."""

        return self.get_by_name(name) is not None

    def exists_by_code(self, code: str) -> bool:
        """Check whether a department code is already in use."""

        return self.get_by_code(code) is not None

    def list_departments(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        status: str | None = None,
    ) -> tuple[list[Department], int]:
        """Return a paginated department list and total count."""

        filters = []
        if search:
            search_term = f"%{search.strip()}%"
            filters.append(
                or_(
                    Department.name.ilike(search_term),
                    Department.code.ilike(search_term),
                    Department.status.ilike(search_term),
                )
            )
        if status:
            filters.append(func.lower(Department.status) == status.lower())

        total_statement = select(func.count()).select_from(Department)
        data_statement = select(Department)

        if filters:
            total_statement = total_statement.where(*filters)
            data_statement = data_statement.where(*filters)

        sort_expression = resolve_sort_expression(
            sort,
            {
                "name": Department.name,
                "code": Department.code,
                "status": Department.status,
                "created_at": Department.created_at,
                "updated_at": Department.updated_at,
            },
            default_key="created_at",
        )

        data_statement = (
            data_statement.order_by(sort_expression)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        total = int(self.session.execute(total_statement).scalar_one())
        departments = list(self.session.execute(data_statement).scalars().all())
        return departments, total

    def count_employees(self, department_id: UUID) -> int:
        """Count employees assigned to a department."""

        statement = select(func.count()).select_from(User).where(User.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def create(self, department: Department) -> Department:
        """Persist a new department."""

        self.session.add(department)
        self.session.flush()
        self.session.refresh(department)
        return department

    def soft_delete(self, department: Department) -> Department:
        """Mark a department as deleted without removing the row."""

        department.status = "deleted"
        self.session.add(department)
        self.session.flush()
        self.session.refresh(department)
        return department
