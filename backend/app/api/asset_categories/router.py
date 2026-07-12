"""Asset category API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.asset_categories.schema import APIResponse, CategoryCreate, CategoryResponse, CategoryUpdate, PaginatedResponse
from app.database.session import get_db
from app.dependencies.auth import RequireRole, get_current_active_user
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.services.asset_category_service import AssetCategoryService

router = APIRouter(prefix="/api/v1/asset-categories", tags=["Asset Categories"])


def get_category_service(db: Session = Depends(get_db)) -> AssetCategoryService:
    """Create the asset category service for the current request."""

    return AssetCategoryService(AssetCategoryRepository(db))


@router.get("", response_model=APIResponse[PaginatedResponse[CategoryResponse]])
def list_categories(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort: str = Query(default="-created_at"),
    status: str | None = Query(default=None),
    _current_user=Depends(get_current_active_user),
    service: AssetCategoryService = Depends(get_category_service),
) -> APIResponse[PaginatedResponse[CategoryResponse]]:
    """List asset categories with search, sort, and pagination."""

    data = service.list_categories(page=page, page_size=page_size, search=search, sort=sort, status_filter=status)
    return APIResponse(message="Categories retrieved successfully", data=data)


@router.get("/{category_id}", response_model=APIResponse[CategoryResponse])
def get_category(
    category_id: UUID,
    _current_user=Depends(get_current_active_user),
    service: AssetCategoryService = Depends(get_category_service),
) -> APIResponse[CategoryResponse]:
    """Retrieve a single asset category by id."""

    return APIResponse(message="Category retrieved successfully", data=service.get_category(category_id))


@router.post("", response_model=APIResponse[CategoryResponse], status_code=201)
def create_category(
    payload: CategoryCreate,
    actor=Depends(RequireRole("Admin")),
    service: AssetCategoryService = Depends(get_category_service),
) -> APIResponse[CategoryResponse]:
    """Create an asset category."""

    return APIResponse(message="Category created successfully", data=service.create_category(payload, actor))


@router.put("/{category_id}", response_model=APIResponse[CategoryResponse])
def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    actor=Depends(RequireRole("Admin")),
    service: AssetCategoryService = Depends(get_category_service),
) -> APIResponse[CategoryResponse]:
    """Update an asset category."""

    return APIResponse(message="Category updated successfully", data=service.update_category(category_id, payload, actor))


@router.delete("/{category_id}", response_model=APIResponse[dict[str, str]])
def delete_category(
    category_id: UUID,
    actor=Depends(RequireRole("Admin")),
    service: AssetCategoryService = Depends(get_category_service),
) -> APIResponse[dict[str, str]]:
    """Soft delete an asset category."""

    return APIResponse(message="Category deleted successfully", data=service.delete_category(category_id, actor))
"""Asset categories API router placeholder."""
