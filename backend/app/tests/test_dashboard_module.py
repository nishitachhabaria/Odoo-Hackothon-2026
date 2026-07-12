"""Dashboard module tests for AssetFlow."""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

from app.main import app
from app.services.dashboard_service import DashboardService


@dataclass
class FakeDashboardRepository:
    """Lightweight fake repository for service tests."""

    last_department_scope: object | None = None
    last_user_scope: object | None = None
    last_activity_scope: tuple[object | None, object | None, int] | None = None

    def get_organization_metrics(self, department_id=None):
        self.last_department_scope = department_id
        return {"departments": 5 if department_id is None else 1, "employees": 125 if department_id is None else 12, "asset_categories": 8}

    def get_user_metrics(self, department_id=None):
        self.last_user_scope = department_id
        return {"active": 118 if department_id is None else 9, "inactive": 7 if department_id is None else 3}

    def get_asset_metrics(self, department_id=None):
        self.last_department_scope = department_id
        return {"total": 42 if department_id is None else 6, "available": 30 if department_id is None else 4, "allocated": 8 if department_id is None else 1, "maintenance": 4 if department_id is None else 1}

    def get_booking_metrics(self, department_id=None):
        return {"today": 0, "active": 0}

    def get_maintenance_metrics(self, department_id=None):
        return {"pending": 0, "approved": 0}

    def get_audit_metrics(self, department_id=None):
        return {"running": 0}

    def get_notification_metrics(self, user_id=None):
        self.last_user_scope = user_id
        return {"unread": 0}

    def get_recent_notifications(self, user_id=None, limit=20):
        return []

    def get_recent_activity(self, department_id=None, user_id=None, limit=20):
        self.last_activity_scope = (department_id, user_id, limit)
        return [
            {
                "title": "Department Created",
                "description": "Human Resources",
                "entity_type": "department",
                "entity_id": "11111111-1111-1111-1111-111111111111",
                "timestamp": "2026-07-12T10:00:00Z",
                "actor": "System Admin",
            }
        ]

    def get_department_chart(self, department_id=None):
        return [{"label": "Operations", "value": 7}]

    def get_user_chart(self, department_id=None):
        self.last_user_scope = department_id
        return {"active": 4, "inactive": 1}

    def get_category_chart(self, department_id=None):
        return [{"label": "Laptop", "value": 15}]

    def count_asset_categories(self):
        return 8


def _make_user(role_name: str, department_id: str | None = None, is_active: bool = True):
    return SimpleNamespace(
        id="22222222-2222-2222-2222-222222222222",
        department_id=department_id,
        is_active=is_active,
        role=SimpleNamespace(name=role_name),
    )


def test_dashboard_scopes_department_head_data():
    """Department heads should receive department-scoped counts."""

    repo = FakeDashboardRepository()
    service = DashboardService(repo)
    response = service.get_dashboard(_make_user("Department Head", department_id="33333333-3333-3333-3333-333333333333"))

    assert response.organization.departments == 1
    assert response.users.active == 9
    assert response.assets.total == 6
    assert repo.last_activity_scope[0] == "33333333-3333-3333-3333-333333333333"


def test_dashboard_scopes_employee_personal_data():
    """Employees should receive a personal dashboard with department scope."""

    repo = FakeDashboardRepository()
    service = DashboardService(repo)
    response = service.get_kpi(_make_user("Employee", department_id="44444444-4444-4444-4444-444444444444"))

    assert response.total_departments == 1
    assert response.employees == 1
    assert response.assets == 6


def test_dashboard_routes_registered_in_app():
    """The dashboard router should be mounted on the application."""

    assert app.url_path_for("read_dashboard") == "/api/v1/dashboard"
