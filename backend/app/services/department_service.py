"""Department service layer for AssetFlow organization setup."""

from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException, status

from app.models import Department, User
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate

logger = logging.getLogger(__name__)


class DepartmentService:
    """Encapsulate department business rules and persistence orchestration."""

    def __init__(self, department_repository: DepartmentRepository, user_repository: UserRepository) -> None:
        self.department_repository = department_repository
        self.user_repository = user_repository

    def list_departments(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        status_filter: str | None = None,
    ) -> PaginatedResponse[DepartmentResponse]:
        """Return a paginated list of departments."""

        departments, total = self.department_repository.list_departments(
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            status=status_filter,
        )
        return PaginatedResponse.from_total(
            items=[DepartmentResponse.model_validate(department) for department in departments],
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_department(self, department_id: UUID) -> DepartmentResponse:
        """Return a department by id."""

        department = self._ensure_department_exists(department_id)
        return DepartmentResponse.model_validate(department)

    def create_department(self, payload: DepartmentCreate, actor: User) -> DepartmentResponse:
        """Create a new department after validation."""

        self._ensure_unique_name_and_code(payload.name, payload.code)
        self._ensure_parent_department_valid(payload.parent_department_id)
        self._ensure_department_head_valid(payload.department_head_id)

        department = Department(
            name=payload.name,
            code=payload.code,
            description=payload.description,
            parent_department_id=payload.parent_department_id,
            department_head_id=payload.department_head_id,
            status="active",
        )
        created = self.department_repository.create(department)
        self.department_repository.session.commit()
        logger.info("Department Created by %s: %s", actor.email, created.name)
        return DepartmentResponse.model_validate(created)

    def update_department(
        self,
        department_id: UUID,
        payload: DepartmentUpdate,
        actor: User,
    ) -> DepartmentResponse:
        """Update a department with validation."""

        department = self._ensure_department_exists(department_id)
        if payload.name and payload.name.lower() != department.name.lower():
            self._ensure_unique_name(payload.name)
            department.name = payload.name
        if payload.code and payload.code.lower() != department.code.lower():
            self._ensure_unique_code(payload.code)
            department.code = payload.code
        if payload.description is not None:
            department.description = payload.description
        if payload.parent_department_id is not None:
            self._ensure_parent_department_valid(payload.parent_department_id, department.id)
            department.parent_department_id = payload.parent_department_id
        if payload.department_head_id is not None:
            self._ensure_department_head_valid(payload.department_head_id)
            department.department_head_id = payload.department_head_id
        if payload.status is not None:
            department.status = payload.status

        self.department_repository.session.add(department)
        self.department_repository.session.commit()
        logger.info("Department Updated by %s: %s", actor.email, department.name)
        return DepartmentResponse.model_validate(department)

    def delete_department(self, department_id: UUID, actor: User) -> dict[str, str]:
        """Soft delete a department after ensuring it has no employees."""

        department = self._ensure_department_exists(department_id)
        employee_count = self.department_repository.count_employees(department.id)
        if employee_count > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete department with employees",
            )

        self.department_repository.soft_delete(department)
        self.department_repository.session.commit()
        logger.info("Department Deleted by %s: %s", actor.email, department.name)
        return {"message": "Department deleted successfully"}

    def _ensure_department_exists(self, department_id: UUID) -> Department:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        return department

    def _ensure_unique_name_and_code(self, name: str, code: str) -> None:
        self._ensure_unique_name(name)
        self._ensure_unique_code(code)

    def _ensure_unique_name(self, name: str) -> None:
        if self.department_repository.exists_by_name(name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department already exists")

    def _ensure_unique_code(self, code: str) -> None:
        if self.department_repository.exists_by_code(code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department code already exists")

    def _ensure_parent_department_valid(self, parent_department_id: UUID | None, current_department_id: UUID | None = None) -> None:
        if parent_department_id is None:
            return
        if current_department_id is not None and parent_department_id == current_department_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Department cannot be its own parent")
        parent_department = self.department_repository.get_by_id(parent_department_id)
        if parent_department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent department not found")
        if parent_department.status.lower() != "active":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cannot assign inactive department")

    def _ensure_department_head_valid(self, department_head_id: UUID | None) -> None:
        if department_head_id is None:
            return
        department_head = self.user_repository.get_by_id(department_head_id)
        if department_head is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department head not found")
        if not department_head.is_active:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cannot assign inactive department head")
        if department_head.role.name != "Department Head":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Department head must have the Department Head role",
            )
