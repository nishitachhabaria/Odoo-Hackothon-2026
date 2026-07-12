"""Dashboard repository for aggregate queries only."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import String, case, cast, func, literal, select, union_all
from sqlalchemy.orm import Session

from app.models import Asset, AssetCategory, AssetStatus, Department, User
from app.repositories.base import BaseRepository


class DashboardRepository(BaseRepository[object]):
    """Repository for dashboard aggregates and timeline queries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_organization_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return organization counts for the current scope."""

        return {
            "departments": self.count_departments(department_id),
            "employees": self.count_employees(department_id),
            "asset_categories": self.count_asset_categories(),
        }

    def get_user_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return user status counts for the current scope."""

        return {
            "active": self.count_active_users(department_id),
            "inactive": self.count_inactive_users(department_id),
        }

    def get_asset_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return asset status counts for the current scope."""

        return {
            "total": self.count_assets(department_id),
            "available": self.count_assets_by_status(AssetStatus.AVAILABLE, department_id),
            "allocated": self.count_assets_by_status(AssetStatus.ALLOCATED, department_id),
            "maintenance": self.count_assets_by_status(AssetStatus.UNDER_MAINTENANCE, department_id),
        }

    def get_booking_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return booking counters.

        Booking tables are not part of the current schema, so this remains a
        safe zeroed placeholder until that module is introduced.
        """

        return {"today": 0, "active": 0}

    def get_maintenance_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return maintenance counters.

        Maintenance tables are not part of the current schema, so this remains a
        safe zeroed placeholder until that module is introduced.
        """

        return {"pending": 0, "approved": 0}

    def get_audit_metrics(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return audit counters.

        Audit tables are not part of the current schema, so this remains a safe
        zeroed placeholder until that module is introduced.
        """

        return {"running": 0}

    def get_notification_metrics(self, user_id: UUID | None = None) -> dict[str, int]:
        """Return notification counters.

        Notification tables are not part of the current schema, so this remains a
        safe zeroed placeholder until that module is introduced.
        """

        return {"unread": 0}

    def get_recent_notifications(self, user_id: UUID | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """Return the most recent notifications.

        The current schema has no notification table yet, so the repository
        returns an empty list while preserving the contract for future wiring.
        """

        return []

    def get_recent_activity(
        self,
        department_id: UUID | None = None,
        user_id: UUID | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Return the latest cross-module activity entries."""

        statements = [
            self._department_activity_queries(department_id),
            self._user_activity_queries(department_id),
            self._category_activity_queries(),
            self._asset_activity_queries(department_id),
        ]
        merged = union_all(*statements).subquery()
        statement = select(
            merged.c.entity_id,
            merged.c.timestamp,
            merged.c.entity_type,
            merged.c.title,
            merged.c.description,
            merged.c.actor,
        ).order_by(merged.c.timestamp.desc()).limit(limit)
        rows = self.session.execute(statement).mappings().all()
        return [dict(row) for row in rows]

    def get_department_chart(self, department_id: UUID | None = None) -> list[dict[str, Any]]:
        """Return department counts suitable for charting."""

        statement = (
            select(
                Department.name.label("label"),
                func.count(User.id).label("value"),
            )
            .outerjoin(User, User.department_id == Department.id)
            .where(Department.status != "deleted")
            .group_by(Department.id, Department.name)
            .order_by(Department.name.asc())
        )
        if department_id is not None:
            statement = statement.where(Department.id == department_id)

        rows = self.session.execute(statement).all()
        return [{"label": label, "value": int(value)} for label, value in rows]

    def get_user_chart(self, department_id: UUID | None = None) -> dict[str, int]:
        """Return active/inactive user counts suitable for charting."""

        active_count = self.count_active_users(department_id)
        inactive_count = self.count_inactive_users(department_id)
        return {"active": active_count, "inactive": inactive_count}

    def get_category_chart(self, department_id: UUID | None = None) -> list[dict[str, Any]]:
        """Return category-to-asset counts suitable for charting."""

        statement = (
            select(
                AssetCategory.name.label("label"),
                func.count(Asset.id).label("value"),
            )
            .outerjoin(Asset, Asset.category_id == AssetCategory.id)
            .where(AssetCategory.status != "deleted")
            .group_by(AssetCategory.id, AssetCategory.name)
            .order_by(func.count(Asset.id).desc(), AssetCategory.name.asc())
        )
        if department_id is not None:
            statement = statement.where(Asset.department_id == department_id)

        rows = self.session.execute(statement).all()
        return [{"label": label, "value": int(value)} for label, value in rows]

    def count_departments(self, department_id: UUID | None = None) -> int:
        """Count active departments."""

        statement = select(func.count()).select_from(Department).where(Department.status != "deleted")
        if department_id is not None:
            statement = statement.where(Department.id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def count_employees(self, department_id: UUID | None = None) -> int:
        """Count users in the current scope."""

        statement = select(func.count()).select_from(User)
        if department_id is not None:
            statement = statement.where(User.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def count_active_users(self, department_id: UUID | None = None) -> int:
        """Count active users in the current scope."""

        statement = select(func.count()).select_from(User).where(User.is_active.is_(True))
        if department_id is not None:
            statement = statement.where(User.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def count_inactive_users(self, department_id: UUID | None = None) -> int:
        """Count inactive users in the current scope."""

        statement = select(func.count()).select_from(User).where(User.is_active.is_(False))
        if department_id is not None:
            statement = statement.where(User.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def count_asset_categories(self) -> int:
        """Count active asset categories."""

        statement = select(func.count()).select_from(AssetCategory).where(AssetCategory.status != "deleted")
        return int(self.session.execute(statement).scalar_one())

    def count_assets(self, department_id: UUID | None = None) -> int:
        """Count assets in the current scope."""

        statement = select(func.count()).select_from(Asset)
        if department_id is not None:
            statement = statement.where(Asset.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def count_assets_by_status(self, status: AssetStatus, department_id: UUID | None = None) -> int:
        """Count assets by lifecycle status."""

        statement = select(func.count()).select_from(Asset).where(Asset.status == status)
        if department_id is not None:
            statement = statement.where(Asset.department_id == department_id)
        return int(self.session.execute(statement).scalar_one())

    def _department_activity_queries(self, department_id: UUID | None = None):
        created = select(
            Department.id.label("entity_id"),
            Department.created_at.label("timestamp"),
            literal("Department").label("entity_type"),
            literal("Department Created").label("title"),
            Department.name.label("description"),
            literal(None).label("actor"),
        ).where(Department.status != "deleted")
        updated = select(
            Department.id.label("entity_id"),
            Department.updated_at.label("timestamp"),
            literal("Department").label("entity_type"),
            literal("Department Updated").label("title"),
            Department.name.label("description"),
            literal(None).label("actor"),
        ).where(Department.status != "deleted", Department.updated_at > Department.created_at)
        if department_id is not None:
            created = created.where(Department.id == department_id)
            updated = updated.where(Department.id == department_id)
        return union_all(created, updated)

    def _user_activity_queries(self, department_id: UUID | None = None):
        created = select(
            User.id.label("entity_id"),
            User.created_at.label("timestamp"),
            literal("User").label("entity_type"),
            literal("Employee Added").label("title"),
            func.concat(User.first_name, literal(" "), User.last_name).label("description"),
            func.concat(User.first_name, literal(" "), User.last_name).label("actor"),
        )
        updated = select(
            User.id.label("entity_id"),
            User.updated_at.label("timestamp"),
            literal("User").label("entity_type"),
            literal("Employee Updated").label("title"),
            func.concat(User.first_name, literal(" "), User.last_name).label("description"),
            func.concat(User.first_name, literal(" "), User.last_name).label("actor"),
        ).where(User.updated_at > User.created_at)
        if department_id is not None:
            created = created.where(User.department_id == department_id)
            updated = updated.where(User.department_id == department_id)
        return union_all(created, updated)

    def _category_activity_queries(self):
        created = select(
            AssetCategory.id.label("entity_id"),
            AssetCategory.created_at.label("timestamp"),
            literal("AssetCategory").label("entity_type"),
            literal("Category Created").label("title"),
            AssetCategory.name.label("description"),
            literal(None).label("actor"),
        ).where(AssetCategory.status != "deleted")
        updated = select(
            AssetCategory.id.label("entity_id"),
            AssetCategory.updated_at.label("timestamp"),
            literal("AssetCategory").label("entity_type"),
            literal("Category Updated").label("title"),
            AssetCategory.name.label("description"),
            literal(None).label("actor"),
        ).where(AssetCategory.status != "deleted", AssetCategory.updated_at > AssetCategory.created_at)
        return union_all(created, updated)

    def _asset_activity_queries(self, department_id: UUID | None = None):
        created = select(
            Asset.id.label("entity_id"),
            Asset.created_at.label("timestamp"),
            literal("Asset").label("entity_type"),
            literal("Asset Registered").label("title"),
            Asset.name.label("description"),
            literal(None).label("actor"),
        )
        updated = select(
            Asset.id.label("entity_id"),
            Asset.updated_at.label("timestamp"),
            literal("Asset").label("entity_type"),
            literal("Asset Updated").label("title"),
            Asset.name.label("description"),
            literal(None).label("actor"),
        ).where(Asset.updated_at > Asset.created_at)
        if department_id is not None:
            created = created.where(Asset.department_id == department_id)
            updated = updated.where(Asset.department_id == department_id)
        return union_all(created, updated)
