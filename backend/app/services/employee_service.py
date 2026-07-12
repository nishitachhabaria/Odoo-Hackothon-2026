"""Employee directory service layer for AssetFlow."""

from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException, status

from app.models import User
from app.repositories.department_repository import DepartmentRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.employee import EmployeeResponse, EmployeeUpdate

logger = logging.getLogger(__name__)


class EmployeeService:
    """Encapsulate employee directory validation and persistence."""

    def __init__(
        self,
        user_repository: UserRepository,
        department_repository: DepartmentRepository,
        role_repository: RoleRepository,
    ) -> None:
        self.user_repository = user_repository
        self.department_repository = department_repository
        self.role_repository = role_repository

    def list_employees(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        department_id: UUID | None = None,
        role_name: str | None = None,
    ) -> PaginatedResponse[EmployeeResponse]:
        """Return a paginated list of employees."""

        employees, total = self.user_repository.list_directory(
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            department_id=department_id,
            role_name=role_name,
        )
        return PaginatedResponse.from_total(
            items=[EmployeeResponse.model_validate(employee) for employee in employees],
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_employee(self, employee_id: UUID) -> EmployeeResponse:
        """Return an employee by UUID."""

        employee = self._ensure_employee_exists(employee_id)
        return EmployeeResponse.model_validate(employee)

    def update_employee(self, employee_id: UUID, payload: EmployeeUpdate, actor: User) -> EmployeeResponse:
        """Update employee directory fields and enforce admin-only role changes."""

        employee = self._ensure_employee_exists(employee_id)

        if payload.department_id is not None:
            self._ensure_department_is_active(payload.department_id)
            employee.department_id = payload.department_id

        if payload.role_id is not None:
            self._ensure_role_exists(payload.role_id)
            if employee.role_id != payload.role_id:
                logger.info(
                    "Role Changed by %s: %s from role_id=%s to role_id=%s",
                    actor.email,
                    employee.email,
                    employee.role_id,
                    payload.role_id,
                )
            employee.role_id = payload.role_id

        for field_name in ("first_name", "last_name", "employee_code", "designation", "joining_date", "phone", "profile_image", "status"):
            value = getattr(payload, field_name)
            if value is not None:
                setattr(employee, field_name, value)

        self.user_repository.update(employee)
        self.user_repository.session.commit()
        return EmployeeResponse.model_validate(employee)

    def _ensure_employee_exists(self, employee_id: UUID) -> User:
        employee = self.user_repository.get_by_id(employee_id)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return employee

    def _ensure_department_is_active(self, department_id: UUID) -> None:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        if department.status.lower() != "active":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cannot assign inactive department")

    def _ensure_role_exists(self, role_id: int) -> None:
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
