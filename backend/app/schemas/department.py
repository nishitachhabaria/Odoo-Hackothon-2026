"""Department schemas for AssetFlow organization setup."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DepartmentReference(BaseModel):
    """Minimal department payload used in nested responses."""

    id: UUID
    name: str
    code: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class DepartmentCreate(BaseModel):
    """Payload used to create a department."""

    name: str = Field(min_length=2, max_length=150, examples=["Human Resources"])
    code: str = Field(min_length=2, max_length=50, examples=["HR"])
    description: str | None = Field(default=None, max_length=500)
    parent_department_id: UUID | None = None
    department_head_id: UUID | None = None

    @field_validator("name", "code")
    @classmethod
    def normalize_value(cls, value: str) -> str:
        """Trim and normalize string fields."""

        return value.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Human Resources",
                "code": "HR",
                "description": "Responsible for people operations",
                "parent_department_id": None,
                "department_head_id": None,
            }
        }
    )


class DepartmentUpdate(BaseModel):
    """Payload used to update a department."""

    name: str | None = Field(default=None, min_length=2, max_length=150)
    code: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    parent_department_id: UUID | None = None
    department_head_id: UUID | None = None
    status: str | None = Field(default=None, max_length=50)

    @field_validator("name", "code", "status")
    @classmethod
    def normalize_optional_value(cls, value: str | None) -> str | None:
        """Trim string fields when provided."""

        return value.strip() if value else value


class DepartmentResponse(BaseModel):
    """Department payload returned to clients."""

    id: UUID
    name: str
    code: str
    description: str | None = None
    parent_department_id: UUID | None = None
    parent_department: DepartmentReference | None = None
    department_head_id: UUID | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
