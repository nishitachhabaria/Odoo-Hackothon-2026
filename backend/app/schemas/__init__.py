"""Schema exports for AssetFlow authentication, RBAC, organization setup, assets, and dashboard."""

from app.schemas.asset import AssetCreate, AssetListResponse, AssetResponse, AssetSearchResponse, AssetUpdate
from app.schemas.asset_category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.auth import RoleResponse, Token, TokenData, UserCreate, UserLogin, UserResponse
from app.schemas.common import PaginationMeta, PaginatedResponse
from app.schemas.dashboard import (
	ActivityItem,
	ActivityResponse,
	ChartDataset,
	ChartResponse,
	DashboardAssetSummary,
	DashboardAuditSummary,
	DashboardBookingSummary,
	DashboardNotificationSummary,
	DashboardOrganizationSummary,
	DashboardResponse,
	DashboardUserSummary,
	KPIResponse,
	NotificationItem,
	NotificationResponse,
)
from app.schemas.department import DepartmentCreate, DepartmentReference, DepartmentResponse, DepartmentUpdate
from app.schemas.employee import EmployeeResponse, EmployeeUpdate
