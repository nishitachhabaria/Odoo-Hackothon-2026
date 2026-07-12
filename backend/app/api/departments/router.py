"""Department API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.departments.schema import APIResponse, DepartmentCreate, DepartmentResponse, DepartmentUpdate, PaginatedResponse
from app.database.session import get_db
from app.dependencies.auth import RequireRole, get_current_active_user
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/api/v1/departments", tags=["Departments"])


def get_department_service(db: Session = Depends(get_db)) -> DepartmentService:
    """Create the department service for the current request."""

    return DepartmentService(DepartmentRepository(db), UserRepository(db))


@router.get("", response_model=APIResponse[PaginatedResponse[DepartmentResponse]])
def list_departments(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort: str = Query(default="-created_at"),
    status: str | None = Query(default=None),
    _current_user=Depends(get_current_active_user),
    service: DepartmentService = Depends(get_department_service),
) -> APIResponse[PaginatedResponse[DepartmentResponse]]:
    """List departments with search, sort, and pagination."""

    data = service.list_departments(page=page, page_size=page_size, search=search, sort=sort, status_filter=status)
    return APIResponse(message="Departments retrieved successfully", data=data)


@router.get("/{department_id}", response_model=APIResponse[DepartmentResponse])
def get_department(
    department_id: UUID,
    _current_user=Depends(get_current_active_user),
    service: DepartmentService = Depends(get_department_service),
) -> APIResponse[DepartmentResponse]:
    """Retrieve a single department by id."""

    return APIResponse(message="Department retrieved successfully", data=service.get_department(department_id))


@router.post("", response_model=APIResponse[DepartmentResponse], status_code=201)
def create_department(
    payload: DepartmentCreate,
    actor=Depends(RequireRole("Admin")),
    service: DepartmentService = Depends(get_department_service),
) -> APIResponse[DepartmentResponse]:
    """Create a department."""

    return APIResponse(message="Department created successfully", data=service.create_department(payload, actor))


@router.put("/{department_id}", response_model=APIResponse[DepartmentResponse])
def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    actor=Depends(RequireRole("Admin")),
    service: DepartmentService = Depends(get_department_service),
) -> APIResponse[DepartmentResponse]:
    """Update a department."""

    return APIResponse(message="Department updated successfully", data=service.update_department(department_id, payload, actor))


@router.delete("/{department_id}", response_model=APIResponse[dict[str, str]])
def delete_department(
    department_id: UUID,
    actor=Depends(RequireRole("Admin")),
    service: DepartmentService = Depends(get_department_service),
) -> APIResponse[dict[str, str]]:
    """Soft delete a department."""

    return APIResponse(message="Department deleted successfully", data=service.delete_department(department_id, actor))
"""Departments API router placeholder."""
