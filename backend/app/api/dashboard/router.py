"""Dashboard API router for role-aware summary endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dashboard.repository import DashboardRepository
from app.api.dashboard.schema import (
	APIResponse,
	ActivityResponse,
	ChartResponse,
	DashboardResponse,
	KPIResponse,
	NotificationResponse,
)
from app.api.dashboard.service import DashboardService
from app.database.session import get_db
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
	"""Create the dashboard service for the current request."""

	return DashboardService(DashboardRepository(db))


@router.get("", response_model=APIResponse[DashboardResponse])
def read_dashboard(
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[DashboardResponse]:
	"""Return the main dashboard summary for the current user."""

	return APIResponse(message="Dashboard retrieved successfully", data=service.get_dashboard(current_user))


@router.get("/recent-activity", response_model=APIResponse[ActivityResponse])
def recent_activity(
	limit: int = Query(default=20, ge=1, le=100),
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[ActivityResponse]:
	"""Return the latest dashboard activity items."""

	return APIResponse(message="Recent activity retrieved successfully", data=service.get_recent_activity(current_user, limit=limit))


@router.get("/notifications", response_model=APIResponse[NotificationResponse])
def notifications(
	limit: int = Query(default=20, ge=1, le=100),
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[NotificationResponse]:
	"""Return unread and recent notifications."""

	return APIResponse(message="Notifications retrieved successfully", data=service.get_notifications(current_user, limit=limit))


@router.get("/kpi", response_model=APIResponse[KPIResponse])
def kpi(
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[KPIResponse]:
	"""Return KPI counters for the current user scope."""

	return APIResponse(message="KPI retrieved successfully", data=service.get_kpi(current_user))


@router.get("/charts/department", response_model=APIResponse[ChartResponse])
def department_chart(
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[ChartResponse]:
	"""Return department chart data."""

	return APIResponse(message="Department chart retrieved successfully", data=service.get_department_chart(current_user))


@router.get("/charts/users", response_model=APIResponse[ChartResponse])
def users_chart(
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[ChartResponse]:
	"""Return user chart data."""

	return APIResponse(message="User chart retrieved successfully", data=service.get_user_chart(current_user))


@router.get("/charts/categories", response_model=APIResponse[ChartResponse])
def categories_chart(
	current_user=Depends(get_current_active_user),
	service: DashboardService = Depends(get_dashboard_service),
) -> APIResponse[ChartResponse]:
	"""Return category chart data."""

	return APIResponse(message="Category chart retrieved successfully", data=service.get_category_chart(current_user))

