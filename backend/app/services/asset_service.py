"""Asset inventory service layer for AssetFlow."""

from __future__ import annotations

import logging
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models import Asset, AssetStatus, User
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.asset import AssetCreate, AssetListResponse, AssetResponse, AssetSearchResponse, AssetUpdate

logger = logging.getLogger(__name__)


class AssetService:
    """Encapsulate asset business rules and persistence orchestration."""

    def __init__(
        self,
        asset_repository: AssetRepository,
        category_repository: AssetCategoryRepository,
        department_repository: DepartmentRepository,
        user_repository: UserRepository,
    ) -> None:
        self.asset_repository = asset_repository
        self.category_repository = category_repository
        self.department_repository = department_repository
        self.user_repository = user_repository

    def list_assets(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        filters: dict[str, object] | None = None,
    ) -> AssetListResponse:
        """Return a paginated list of assets."""

        assets, total = self.asset_repository.list_assets(
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            filters=filters,
        )
        return AssetListResponse.from_total(
            items=[AssetResponse.model_validate(asset) for asset in assets],
            page=page,
            page_size=page_size,
            total=total,
        )

    def search_assets(
        self,
        search: str,
        page: int,
        page_size: int,
        sort: str,
        filters: dict[str, object] | None = None,
    ) -> AssetSearchResponse:
        """Return a paginated asset search result set."""

        assets, total = self.asset_repository.search_assets(
            search=search,
            page=page,
            page_size=page_size,
            sort=sort,
            filters=filters,
        )
        return AssetSearchResponse.from_total(
            items=[AssetResponse.model_validate(asset) for asset in assets],
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_asset(self, asset_id: UUID) -> AssetResponse:
        """Return an asset by id."""

        asset = self._ensure_asset_exists(asset_id)
        return AssetResponse.model_validate(asset)

    def create_asset(self, payload: AssetCreate, actor: User) -> AssetResponse:
        """Create a new asset with an auto-generated asset tag."""

        self._validate_create_payload(payload)
        if self.asset_repository.exists_by_serial_number(payload.serial_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Serial number already exists")

        asset = Asset(
            asset_tag=self.asset_repository.get_next_asset_tag(),
            name=payload.name,
            description=payload.description,
            category_id=payload.category_id,
            department_id=payload.department_id,
            serial_number=payload.serial_number,
            manufacturer=payload.manufacturer,
            model_number=payload.model_number,
            purchase_date=payload.purchase_date,
            purchase_cost=Decimal(payload.purchase_cost),
            warranty_expiry=payload.warranty_expiry,
            condition=payload.condition,
            location=payload.location,
            status=payload.status,
            is_bookable=payload.is_bookable,
            photo_url=payload.photo_url,
            document_url=payload.document_url,
            created_by=actor.id,
            updated_by=actor.id,
        )

        try:
            created = self.asset_repository.create(asset)
            self.asset_repository.session.commit()
        except IntegrityError as exc:
            self.asset_repository.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Asset could not be created") from exc

        logger.info("Asset Created by %s: %s", actor.email, created.asset_tag)
        return AssetResponse.model_validate(created)

    def update_asset(self, asset_id: UUID, payload: AssetUpdate, actor: User) -> AssetResponse:
        """Update an existing asset with validation."""

        asset = self._ensure_asset_exists(asset_id)
        self._apply_updates(asset, payload)
        self._validate_asset(asset, exclude_id=asset.id)
        asset.updated_by = actor.id

        self.asset_repository.update(asset)
        self.asset_repository.session.commit()
        logger.info("Asset Updated by %s: %s", actor.email, asset.asset_tag)
        return AssetResponse.model_validate(asset)

    def delete_asset(self, asset_id: UUID, actor: User) -> dict[str, str]:
        """Retire an asset without dropping the row."""

        asset = self._ensure_asset_exists(asset_id)
        asset.status = AssetStatus.RETIRED
        asset.updated_by = actor.id
        self.asset_repository.update(asset)
        self.asset_repository.session.commit()
        logger.info("Asset Deleted by %s: %s", actor.email, asset.asset_tag)
        return {"message": "Asset retired successfully"}

    def filter_assets(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        filters: dict[str, object] | None = None,
    ) -> AssetListResponse:
        """Return a paginated filtered asset list."""

        return self.list_assets(page=page, page_size=page_size, search=search, sort=sort, filters=filters)

    def _ensure_asset_exists(self, asset_id: UUID) -> Asset:
        asset = self.asset_repository.get_by_id(asset_id)
        if asset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        return asset

    def _validate_create_payload(self, payload: AssetCreate) -> None:
        """Validate create-only asset constraints."""

        self._validate_dates_and_cost(payload.purchase_date, payload.warranty_expiry, payload.purchase_cost)
        self._validate_category_and_department(payload.category_id, payload.department_id)

    def _validate_asset(self, asset: Asset, exclude_id: UUID | None = None) -> None:
        """Validate persisted asset constraints."""

        self._validate_dates_and_cost(asset.purchase_date, asset.warranty_expiry, asset.purchase_cost)
        existing = self.asset_repository.get_by_serial_number(asset.serial_number)
        if existing is not None and existing.id != exclude_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Serial number already exists")
        self._validate_category_and_department(asset.category_id, asset.department_id)

    def _validate_category_and_department(self, category_id: UUID, department_id: UUID | None) -> None:
        if self.category_repository.get_by_id(category_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if department_id is not None and self.department_repository.get_by_id(department_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    def _validate_dates_and_cost(self, purchase_date, warranty_expiry, purchase_cost) -> None:
        if purchase_cost is not None and Decimal(purchase_cost) < 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Purchase cost cannot be negative")
        if purchase_date and warranty_expiry and warranty_expiry < purchase_date:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Warranty expiry cannot be before purchase date")

    def _apply_updates(self, asset: Asset, payload: AssetUpdate) -> None:
        updates = payload.model_dump(exclude_unset=True)
        for field_name, value in updates.items():
            if field_name == "purchase_cost" and value is not None:
                setattr(asset, field_name, Decimal(value))
            else:
                setattr(asset, field_name, value)
