"""Asset inventory API router."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.assets.repository import AssetRepository
from app.api.assets.schema import APIResponse, AssetCreate, AssetListResponse, AssetResponse, AssetSearchResponse, AssetUpdate
from app.api.assets.service import AssetService
from app.api.asset_categories.repository import AssetCategoryRepository
from app.database.session import get_db
from app.dependencies.auth import RequireRole, get_current_active_user
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/api/v1/assets", tags=["Assets"])


def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    """Create the asset service for the current request."""

    return AssetService(
        AssetRepository(db),
        AssetCategoryRepository(db),
        DepartmentRepository(db),
        UserRepository(db),
    )


@router.get("/search", response_model=APIResponse[AssetSearchResponse])
def search_assets(
    search: str = Query(..., min_length=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort: str = Query(default="-created_at"),
    _current_user=Depends(get_current_active_user),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetSearchResponse]:
    """Search assets by the supported inventory fields."""

    data = service.search_assets(search=search, page=page, page_size=page_size, sort=sort)
    return APIResponse(message="Asset search completed successfully", data=data)


@router.get("/filter", response_model=APIResponse[AssetListResponse])
def filter_assets(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort: str = Query(default="-created_at"),
    status: str | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    department_id: UUID | None = Query(default=None),
    condition: str | None = Query(default=None),
    is_bookable: bool | None = Query(default=None),
    purchase_date_from: date | None = Query(default=None),
    purchase_date_to: date | None = Query(default=None),
    warranty_expiry_from: date | None = Query(default=None),
    warranty_expiry_to: date | None = Query(default=None),
    _current_user=Depends(get_current_active_user),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetListResponse]:
    """Filter assets by inventory fields."""

    filters = {
        "status": status,
        "category_id": category_id,
        "department_id": department_id,
        "condition": condition,
        "is_bookable": is_bookable,
        "purchase_date_from": purchase_date_from,
        "purchase_date_to": purchase_date_to,
        "warranty_expiry_from": warranty_expiry_from,
        "warranty_expiry_to": warranty_expiry_to,
    }
    data = service.filter_assets(page=page, page_size=page_size, search=search, sort=sort, filters=filters)
    return APIResponse(message="Assets filtered successfully", data=data)


@router.get("", response_model=APIResponse[AssetListResponse])
def list_assets(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort: str = Query(default="-created_at"),
    _current_user=Depends(get_current_active_user),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetListResponse]:
    """List assets with pagination, search, and sorting."""

    data = service.list_assets(page=page, page_size=page_size, search=search, sort=sort)
    return APIResponse(message="Assets retrieved successfully", data=data)


@router.get("/{asset_id}", response_model=APIResponse[AssetResponse])
def get_asset(
    asset_id: UUID,
    _current_user=Depends(get_current_active_user),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetResponse]:
    """Retrieve a single asset by id."""

    return APIResponse(message="Asset retrieved successfully", data=service.get_asset(asset_id))


@router.post("", response_model=APIResponse[AssetResponse], status_code=201)
def create_asset(
    payload: AssetCreate,
    actor=Depends(RequireRole("Admin", "Asset Manager")),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetResponse]:
    """Create a new asset record."""

    return APIResponse(message="Asset created successfully", data=service.create_asset(payload, actor))


@router.put("/{asset_id}", response_model=APIResponse[AssetResponse])
def update_asset(
    asset_id: UUID,
    payload: AssetUpdate,
    actor=Depends(RequireRole("Admin", "Asset Manager")),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[AssetResponse]:
    """Update an existing asset record."""

    return APIResponse(message="Asset updated successfully", data=service.update_asset(asset_id, payload, actor))


@router.delete("/{asset_id}", response_model=APIResponse[dict[str, str]])
def delete_asset(
    asset_id: UUID,
    actor=Depends(RequireRole("Admin", "Asset Manager")),
    service: AssetService = Depends(get_asset_service),
) -> APIResponse[dict[str, str]]:
    """Retire an asset from the active directory."""

    return APIResponse(message="Asset retired successfully", data=service.delete_asset(asset_id, actor))
