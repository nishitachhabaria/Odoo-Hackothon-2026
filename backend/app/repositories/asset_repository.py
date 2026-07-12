"""Asset repository for database queries only."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import Integer, String, cast, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Asset, AssetCategory, AssetStatus, Department
from app.repositories.base import BaseRepository
from app.utils.querying import resolve_sort_expression


class AssetRepository(BaseRepository[Asset]):
    """Repository for asset persistence and search queries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, asset_id: UUID) -> Asset | None:
        statement = self._base_query().where(Asset.id == asset_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_asset_tag(self, asset_tag: str) -> Asset | None:
        statement = self._base_query().where(Asset.asset_tag == asset_tag)
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_serial_number(self, serial_number: str) -> Asset | None:
        statement = self._base_query().where(func.lower(Asset.serial_number) == serial_number.lower())
        return self.session.execute(statement).scalar_one_or_none()

    def exists_by_serial_number(self, serial_number: str) -> bool:
        return self.get_by_serial_number(serial_number) is not None

    def get_next_asset_tag(self) -> str:
        statement = select(
            func.coalesce(
                func.max(cast(func.regexp_replace(Asset.asset_tag, r"^AF-", ""), Integer)),
                0,
            )
        )
        max_sequence = int(self.session.execute(statement).scalar_one())
        return f"AF-{max_sequence + 1:06d}"

    def list_assets(
        self,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
        filters: dict[str, Any] | None = None,
    ) -> tuple[list[Asset], int]:
        statement_filters = self._build_filters(search, filters or {})
        total_statement = select(func.count()).select_from(Asset).join(AssetCategory).outerjoin(Department)
        data_statement = self._base_query().join(AssetCategory).outerjoin(Department)

        if statement_filters:
            total_statement = total_statement.where(*statement_filters)
            data_statement = data_statement.where(*statement_filters)

        sort_expression = resolve_sort_expression(
            sort,
            {
                "asset_tag": Asset.asset_tag,
                "name": Asset.name,
                "serial_number": Asset.serial_number,
                "manufacturer": Asset.manufacturer,
                "location": Asset.location,
                "status": Asset.status,
                "condition": Asset.condition,
                "created_at": Asset.created_at,
                "updated_at": Asset.updated_at,
                "purchase_date": Asset.purchase_date,
                "warranty_expiry": Asset.warranty_expiry,
            },
            default_key="created_at",
        )
        data_statement = data_statement.order_by(sort_expression).offset((page - 1) * page_size).limit(page_size)

        total = int(self.session.execute(total_statement).scalar_one())
        assets = list(self.session.execute(data_statement).scalars().all())
        return assets, total

    def search_assets(
        self,
        search: str,
        page: int,
        page_size: int,
        sort: str,
        filters: dict[str, Any] | None = None,
    ) -> tuple[list[Asset], int]:
        return self.list_assets(page=page, page_size=page_size, search=search, sort=sort, filters=filters)

    def create(self, asset: Asset) -> Asset:
        self.session.add(asset)
        self.session.flush()
        self.session.refresh(asset)
        return self.get_by_id(asset.id) or asset

    def update(self, asset: Asset) -> Asset:
        self.session.add(asset)
        self.session.flush()
        self.session.refresh(asset)
        return self.get_by_id(asset.id) or asset

    def soft_delete(self, asset: Asset) -> Asset:
        asset.status = AssetStatus.RETIRED
        self.session.add(asset)
        self.session.flush()
        self.session.refresh(asset)
        return asset

    def _base_query(self):
        return select(Asset).options(
            selectinload(Asset.category),
            selectinload(Asset.department),
            selectinload(Asset.created_by_user),
            selectinload(Asset.updated_by_user),
        )

    def _build_filters(self, search: str | None, filters: dict[str, Any]) -> list[Any]:
        conditions: list[Any] = []
        if search:
            term = f"%{search.strip()}%"
            conditions.append(
                or_(
                    Asset.asset_tag.ilike(term),
                    Asset.serial_number.ilike(term),
                    Asset.name.ilike(term),
                    Asset.manufacturer.ilike(term),
                    Asset.model_number.ilike(term),
                    Asset.location.ilike(term),
                    cast(Asset.status, String).ilike(term),
                    cast(Asset.condition, String).ilike(term),
                    AssetCategory.name.ilike(term),
                    AssetCategory.code.ilike(term),
                    Department.name.ilike(term),
                )
            )
        if category_id := filters.get("category_id"):
            conditions.append(Asset.category_id == category_id)
        if department_id := filters.get("department_id"):
            conditions.append(Asset.department_id == department_id)
        if status := filters.get("status"):
            conditions.append(func.lower(cast(Asset.status, String)) == str(status).lower())
        if condition := filters.get("condition"):
            conditions.append(func.lower(cast(Asset.condition, String)) == str(condition).lower())
        if filters.get("is_bookable") is not None:
            conditions.append(Asset.is_bookable == filters["is_bookable"])
        if purchase_date_from := filters.get("purchase_date_from"):
            conditions.append(Asset.purchase_date >= purchase_date_from)
        if purchase_date_to := filters.get("purchase_date_to"):
            conditions.append(Asset.purchase_date <= purchase_date_to)
        if warranty_expiry_from := filters.get("warranty_expiry_from"):
            conditions.append(Asset.warranty_expiry >= warranty_expiry_from)
        if warranty_expiry_to := filters.get("warranty_expiry_to"):
            conditions.append(Asset.warranty_expiry <= warranty_expiry_to)
        return conditions
