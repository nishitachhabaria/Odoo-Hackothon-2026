"""Employee directory schemas for AssetFlow."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.department import DepartmentReference
from app.schemas.auth import RoleResponse


class EmployeeUpdate(BaseModel):
    """Payload used to update employee directory data."""

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    employee_code: str | None = Field(default=None, max_length=50)
    designation: str | None = Field(default=None, max_length=150)
    joining_date: date | None = None
    department_id: UUID | None = None
    phone: str | None = Field(default=None, max_length=30)
    profile_image: str | None = Field(default=None, max_length=500)
    status: str | None = Field(default=None, max_length=50)
    role_id: int | None = None

    @field_validator("first_name", "last_name", "employee_code", "designation", "phone", "profile_image", "status")
    @classmethod
    def normalize_optional_value(cls, value: str | None) -> str | None:
        """Trim string fields when provided."""

        return value.strip() if value else value


class EmployeeResponse(BaseModel):
    """Employee directory payload returned to clients."""

    id: UUID
    first_name: str
    last_name: str
    email: str
    employee_code: str | None = None
    designation: str | None = None
    joining_date: date | None = None
    phone: str | None = None
    profile_image: str | None = None
    department_id: UUID | None = None
    department: DepartmentReference | None = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)
