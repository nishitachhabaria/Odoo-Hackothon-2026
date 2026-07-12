"""Employee directory API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.employees.schema import APIResponse, EmployeeResponse, EmployeeUpdate, PaginatedResponse
from app.database.session import get_db
from app.dependencies.auth import RequireRole, get_current_active_user
from app.repositories.department_repository import DepartmentRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/v1/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Create the employee service for the current request."""

    return EmployeeService(UserRepository(db), DepartmentRepository(db), RoleRepository(db))


@router.get("", response_model=APIResponse[PaginatedResponse[EmployeeResponse]])
def list_employees(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort: str = Query(default="-created_at"),
    department_id: UUID | None = Query(default=None),
    role: str | None = Query(default=None),
    _current_user=Depends(get_current_active_user),
    service: EmployeeService = Depends(get_employee_service),
) -> APIResponse[PaginatedResponse[EmployeeResponse]]:
    """List employees with search, sort, and pagination."""

    data = service.list_employees(
        page=page,
        page_size=page_size,
        search=search,
        sort=sort,
        department_id=department_id,
        role_name=role,
    )
    return APIResponse(message="Employees retrieved successfully", data=data)


@router.get("/{employee_id}", response_model=APIResponse[EmployeeResponse])
def get_employee(
    employee_id: UUID,
    _current_user=Depends(get_current_active_user),
    service: EmployeeService = Depends(get_employee_service),
) -> APIResponse[EmployeeResponse]:
    """Retrieve a single employee by id."""

    return APIResponse(message="Employee retrieved successfully", data=service.get_employee(employee_id))


@router.put("/{employee_id}", response_model=APIResponse[EmployeeResponse])
def update_employee(
    employee_id: UUID,
    payload: EmployeeUpdate,
    actor=Depends(RequireRole("Admin")),
    service: EmployeeService = Depends(get_employee_service),
) -> APIResponse[EmployeeResponse]:
    """Update employee directory details and RBAC assignments."""

    return APIResponse(message="Employee updated successfully", data=service.update_employee(employee_id, payload, actor))
"""Employees API router placeholder."""
