"""Dashboard service layer for AssetFlow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from app.models import User
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import (
    ActivityItem,
    ActivityResponse,
    ChartDataset,
    ChartResponse,
    DashboardAssetSummary,
    DashboardAuditSummary,
    DashboardBookingSummary,
    DashboardMaintenanceSummary,
    DashboardNotificationSummary,
    DashboardOrganizationSummary,
    DashboardResponse,
    DashboardUserSummary,
    KPIResponse,
    NotificationItem,
    NotificationResponse,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DashboardScope:
    """Resolved dashboard visibility scope for a user."""

    role_name: str
    user_id: UUID
    department_id: UUID | None

    @property
    def is_admin(self) -> bool:
        return self.role_name == "admin"

    @property
    def is_department_head(self) -> bool:
        return self.role_name == "department head"

    @property
    def is_asset_manager(self) -> bool:
        return self.role_name == "asset manager"

    @property
    def is_employee(self) -> bool:
        return self.role_name == "employee"


class DashboardService:
    """Combine dashboard repository metrics into API responses.

    The service is intentionally prepared for future Redis caching by keeping a
    cache backend hook and cache key helpers, but no Redis dependency is
    introduced yet.
    """

    cache_ttl_seconds = 300

    def __init__(self, dashboard_repository: DashboardRepository) -> None:
        self.dashboard_repository = dashboard_repository
        self.cache_backend = None

    def get_dashboard(self, current_user: User) -> DashboardResponse:
        """Return the dashboard payload for the current user role."""

        scope = self._resolve_scope(current_user)
        organization = self._build_organization_summary(scope)
        users = self._build_user_summary(scope)
        assets = self._build_asset_summary(scope)
        self.dashboard_repository.get_recent_activity(scope.department_id, scope.user_id, limit=20)

        return DashboardResponse(
            organization=DashboardOrganizationSummary(**organization),
            users=DashboardUserSummary(**users),
            assets=DashboardAssetSummary(**assets),
            bookings=DashboardBookingSummary(**self.dashboard_repository.get_booking_metrics(scope.department_id)),
            maintenance=DashboardMaintenanceSummary(**self.dashboard_repository.get_maintenance_metrics(scope.department_id)),
            audits=DashboardAuditSummary(**self.dashboard_repository.get_audit_metrics(scope.department_id)),
            notifications=DashboardNotificationSummary(**self.dashboard_repository.get_notification_metrics(scope.user_id)),
        )

    def get_kpi(self, current_user: User) -> KPIResponse:
        """Return KPI values for the current user role."""

        scope = self._resolve_scope(current_user)
        organization = self._build_organization_summary(scope)
        users = self._build_user_summary(scope)
        assets = self._build_asset_summary(scope)
        return KPIResponse(
            total_departments=organization["departments"],
            employees=organization["employees"],
            categories=organization["asset_categories"],
            assets=assets["total"],
            active_users=users["active"],
        )

    def get_recent_activity(self, current_user: User, limit: int = 20) -> ActivityResponse:
        """Return the latest activity feed entries."""

        scope = self._resolve_scope(current_user)
        activities = self.dashboard_repository.get_recent_activity(scope.department_id, scope.user_id, limit)
        return ActivityResponse(activities=[ActivityItem.model_validate(item) for item in activities])

    def get_notifications(self, current_user: User, limit: int = 20) -> NotificationResponse:
        """Return unread and recent notifications.

        Notifications are not persisted yet, so unread counts remain zero and
        recent notifications stay empty until the module is introduced.
        """

        scope = self._resolve_scope(current_user)
        metrics = self.dashboard_repository.get_notification_metrics(scope.user_id)
        recent = self.dashboard_repository.get_recent_notifications(scope.user_id, limit)
        return NotificationResponse(
            unread=metrics["unread"],
            recent=[NotificationItem.model_validate(item) for item in recent],
        )

    def get_department_chart(self, current_user: User) -> ChartResponse:
        """Return department chart data."""

        scope = self._resolve_scope(current_user)
        if scope.is_department_head or scope.is_employee:
            chart_rows = self.dashboard_repository.get_department_chart(scope.department_id)
        elif scope.is_asset_manager:
            chart_rows = []
        else:
            chart_rows = self.dashboard_repository.get_department_chart(None)

        return self._to_chart_response(chart_rows, label="Employees")

    def get_user_chart(self, current_user: User) -> ChartResponse:
        """Return user status chart data."""

        scope = self._resolve_scope(current_user)
        if scope.is_asset_manager:
            chart_data = {"active": 0, "inactive": 0}
        else:
            chart_data = self.dashboard_repository.get_user_chart(scope.department_id)

        return ChartResponse(
            labels=["Active", "Inactive"],
            datasets=[ChartDataset(label="Users", data=[chart_data["active"], chart_data["inactive"]])],
        )

    def get_category_chart(self, current_user: User) -> ChartResponse:
        """Return asset category chart data."""

        scope = self._resolve_scope(current_user)
        rows = self.dashboard_repository.get_category_chart(None if scope.is_admin or scope.is_asset_manager else scope.department_id)
        return self._to_chart_response(rows, label="Assets")

    def _resolve_scope(self, current_user: User) -> DashboardScope:
        role_name = current_user.role.name.lower() if current_user.role is not None else "employee"
        return DashboardScope(role_name=role_name, user_id=current_user.id, department_id=current_user.department_id)

    def _build_organization_summary(self, scope: DashboardScope) -> dict[str, int]:
        if scope.is_admin:
            return self.dashboard_repository.get_organization_metrics(None)

        if scope.is_department_head:
            return self.dashboard_repository.get_organization_metrics(scope.department_id)

        if scope.is_asset_manager:
            return {
                "departments": 0,
                "employees": 0,
                "asset_categories": self.dashboard_repository.count_asset_categories(),
            }

        if scope.is_employee:
            return {
                "departments": 1 if scope.department_id is not None else 0,
                "employees": 1,
                "asset_categories": self.dashboard_repository.count_asset_categories(),
            }

        return self.dashboard_repository.get_organization_metrics(scope.department_id)

    def _build_user_summary(self, scope: DashboardScope) -> dict[str, int]:
        if scope.is_admin:
            return self.dashboard_repository.get_user_metrics(None)

        if scope.is_department_head:
            return self.dashboard_repository.get_user_metrics(scope.department_id)

        if scope.is_asset_manager:
            return {"active": 0, "inactive": 0}

        if scope.is_employee:
            return {"active": 1, "inactive": 0}

        return self.dashboard_repository.get_user_metrics(scope.department_id)

    def _build_asset_summary(self, scope: DashboardScope) -> dict[str, int]:
        if scope.is_admin:
            return self.dashboard_repository.get_asset_metrics(None)

        if scope.is_department_head or scope.is_employee:
            return self.dashboard_repository.get_asset_metrics(scope.department_id)

        if scope.is_asset_manager:
            return self.dashboard_repository.get_asset_metrics(None)

        return self.dashboard_repository.get_asset_metrics(scope.department_id)

    def _to_chart_response(self, rows: list[dict[str, int]], label: str) -> ChartResponse:
        """Convert repository rows into a standard chart response."""

        return ChartResponse(
            labels=[row["label"] for row in rows],
            datasets=[ChartDataset(label=label, data=[row["value"] for row in rows])],
        )
