"""Asset category service layer for AssetFlow organization setup."""

from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException, status

from app.models import AssetCategory, User
from app.repositories.asset_category_repository import AssetCategoryRepository
from app.schemas.asset_category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.common import PaginatedResponse

logger = logging.getLogger(__name__)


class AssetCategoryService:
    """Encapsulate asset category business rules and persistence orchestration."""

    def __init__(self, category_repository: AssetCategoryRepository) -> None:
        self.category_repository = category_repository

    def list_categories(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        status_filter: str | None = None,
    ) -> PaginatedResponse[CategoryResponse]:
        """Return a paginated list of categories."""

        categories, total = self.category_repository.list_categories(
            page=page,
            page_size=page_size,
            search=search,
            sort=sort,
            status=status_filter,
        )
        return PaginatedResponse.from_total(
            items=[CategoryResponse.model_validate(category) for category in categories],
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_category(self, category_id: UUID) -> CategoryResponse:
        """Return a category by id."""

        category = self._ensure_category_exists(category_id)
        return CategoryResponse.model_validate(category)

    def create_category(self, payload: CategoryCreate, actor: User) -> CategoryResponse:
        """Create a new asset category after validation."""

        self._ensure_unique_name_and_code(payload.name, payload.code)
        category = AssetCategory(
            name=payload.name,
            code=payload.code,
            description=payload.description,
            default_warranty_months=payload.default_warranty_months,
            is_bookable=payload.is_bookable,
            status="active",
        )
        created = self.category_repository.create(category)
        self.category_repository.session.commit()
        logger.info("Category Created by %s: %s", actor.email, created.name)
        return CategoryResponse.model_validate(created)

    def update_category(
        self,
        category_id: UUID,
        payload: CategoryUpdate,
        actor: User,
    ) -> CategoryResponse:
        """Update an asset category with validation."""

        category = self._ensure_category_exists(category_id)
        if payload.name and payload.name.lower() != category.name.lower():
            self._ensure_unique_name(payload.name)
            category.name = payload.name
        if payload.code and payload.code.lower() != category.code.lower():
            self._ensure_unique_code(payload.code)
            category.code = payload.code
        if payload.description is not None:
            category.description = payload.description
        if payload.default_warranty_months is not None:
            category.default_warranty_months = payload.default_warranty_months
        if payload.is_bookable is not None:
            category.is_bookable = payload.is_bookable
        if payload.status is not None:
            category.status = payload.status

        self.category_repository.session.add(category)
        self.category_repository.session.commit()
        logger.info("Category Updated by %s: %s", actor.email, category.name)
        return CategoryResponse.model_validate(category)

    def delete_category(self, category_id: UUID, actor: User) -> dict[str, str]:
        """Soft delete an asset category."""

        category = self._ensure_category_exists(category_id)
        self.category_repository.soft_delete(category)
        self.category_repository.session.commit()
        logger.info("Category Deleted by %s: %s", actor.email, category.name)
        return {"message": "Category deleted successfully"}

    def _ensure_category_exists(self, category_id: UUID) -> AssetCategory:
        category = self.category_repository.get_by_id(category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    def _ensure_unique_name_and_code(self, name: str, code: str) -> None:
        self._ensure_unique_name(name)
        self._ensure_unique_code(code)

    def _ensure_unique_name(self, name: str) -> None:
        if self.category_repository.exists_by_name(name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

    def _ensure_unique_code(self, code: str) -> None:
        if self.category_repository.exists_by_code(code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category code already exists")
