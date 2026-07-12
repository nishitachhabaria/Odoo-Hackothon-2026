"""Asset category repository for organization setup data access."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import AssetCategory
from app.repositories.base import BaseRepository
from app.utils.querying import resolve_sort_expression


class AssetCategoryRepository(BaseRepository[AssetCategory]):
    """Repository for asset category persistence and search queries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, category_id: UUID) -> AssetCategory | None:
        """Return an asset category by UUID."""

        statement = select(AssetCategory).where(AssetCategory.id == category_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_name(self, name: str) -> AssetCategory | None:
        """Return a category by unique name."""

        statement = select(AssetCategory).where(func.lower(AssetCategory.name) == name.lower())
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_code(self, code: str) -> AssetCategory | None:
        """Return a category by unique code."""

        statement = select(AssetCategory).where(func.lower(AssetCategory.code) == code.lower())
        return self.session.execute(statement).scalar_one_or_none()

    def exists_by_name(self, name: str) -> bool:
        """Check whether a category name is already in use."""

        return self.get_by_name(name) is not None

    def exists_by_code(self, code: str) -> bool:
        """Check whether a category code is already in use."""

        return self.get_by_code(code) is not None

    def list_categories(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        status: str | None = None,
    ) -> tuple[list[AssetCategory], int]:
        """Return a paginated category list and total count."""

        filters = []
        if search:
            search_term = f"%{search.strip()}%"
            filters.append(
                or_(
                    AssetCategory.name.ilike(search_term),
                    AssetCategory.code.ilike(search_term),
                    AssetCategory.status.ilike(search_term),
                )
            )
        if status:
            filters.append(func.lower(AssetCategory.status) == status.lower())

        total_statement = select(func.count()).select_from(AssetCategory)
        data_statement = select(AssetCategory)

        if filters:
            total_statement = total_statement.where(*filters)
            data_statement = data_statement.where(*filters)

        sort_expression = resolve_sort_expression(
            sort,
            {
                "name": AssetCategory.name,
                "code": AssetCategory.code,
                "status": AssetCategory.status,
                "created_at": AssetCategory.created_at,
                "updated_at": AssetCategory.updated_at,
            },
            default_key="created_at",
        )

        data_statement = (
            data_statement.order_by(sort_expression)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        total = int(self.session.execute(total_statement).scalar_one())
        categories = list(self.session.execute(data_statement).scalars().all())
        return categories, total

    def create(self, category: AssetCategory) -> AssetCategory:
        """Persist a new category."""

        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category

    def soft_delete(self, category: AssetCategory) -> AssetCategory:
        """Mark a category as deleted without removing the row."""

        category.status = "deleted"
        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category
