"""Dashboard schemas for AssetFlow."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DashboardOrganizationSummary(BaseModel):
    """Organization-level dashboard summary."""

    departments: int = Field(ge=0)
    employees: int = Field(ge=0)
    asset_categories: int = Field(ge=0)


class DashboardUserSummary(BaseModel):
    """User activity summary for the dashboard."""

    active: int = Field(ge=0)
    inactive: int = Field(ge=0)


class DashboardAssetSummary(BaseModel):
    """Asset inventory summary for the dashboard."""

    total: int = Field(ge=0)
    available: int = Field(ge=0)
    allocated: int = Field(ge=0)
    maintenance: int = Field(ge=0)


class DashboardBookingSummary(BaseModel):
    """Booking summary placeholder for future integration."""

    today: int = Field(ge=0)
    active: int = Field(ge=0)


class DashboardMaintenanceSummary(BaseModel):
    """Maintenance summary placeholder for future integration."""

    pending: int = Field(ge=0)
    approved: int = Field(ge=0)


class DashboardAuditSummary(BaseModel):
    """Audit summary placeholder for future integration."""

    running: int = Field(ge=0)


class DashboardNotificationSummary(BaseModel):
    """Notification summary for the dashboard."""

    unread: int = Field(ge=0)


class DashboardResponse(BaseModel):
    """Top-level dashboard payload."""

    organization: DashboardOrganizationSummary
    users: DashboardUserSummary
    assets: DashboardAssetSummary
    bookings: DashboardBookingSummary
    maintenance: DashboardMaintenanceSummary
    audits: DashboardAuditSummary
    notifications: DashboardNotificationSummary

    model_config = ConfigDict(from_attributes=True)


class KPIResponse(BaseModel):
    """Key performance indicator payload."""

    total_departments: int = Field(ge=0)
    employees: int = Field(ge=0)
    categories: int = Field(ge=0)
    assets: int = Field(ge=0)
    active_users: int = Field(ge=0)


class ActivityItem(BaseModel):
    """Single activity feed item."""

    title: str
    description: str | None = None
    entity_type: str
    entity_id: UUID
    timestamp: datetime
    actor: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ActivityResponse(BaseModel):
    """Recent activity feed payload."""

    activities: list[ActivityItem]


class NotificationItem(BaseModel):
    """Single notification item."""

    id: UUID
    title: str
    message: str
    created_at: datetime
    is_read: bool = False

    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(BaseModel):
    """Notification payload with unread count and recent items."""

    unread: int = Field(ge=0)
    recent: list[NotificationItem]


class ChartDataset(BaseModel):
    """Single chart dataset."""

    label: str
    data: list[int]


class ChartResponse(BaseModel):
    """Frontend-ready chart payload."""

    labels: list[str]
    datasets: list[ChartDataset]
