"""Asset category schemas for AssetFlow organization setup."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    """Payload used to create an asset category."""

    name: str = Field(min_length=2, max_length=150, examples=["Laptop"])
    code: str = Field(min_length=2, max_length=50, examples=["LAPTOP"])
    description: str | None = Field(default=None, max_length=500)
    default_warranty_months: int = Field(default=0, ge=0, le=120)
    is_bookable: bool = False

    @field_validator("name", "code")
    @classmethod
    def normalize_value(cls, value: str) -> str:
        """Trim string fields."""

        return value.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "code": "LAPTOP",
                "description": "Portable computing devices",
                "default_warranty_months": 12,
                "is_bookable": True,
            }
        }
    )


class CategoryUpdate(BaseModel):
    """Payload used to update an asset category."""

    name: str | None = Field(default=None, min_length=2, max_length=150)
    code: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    default_warranty_months: int | None = Field(default=None, ge=0, le=120)
    is_bookable: bool | None = None
    status: str | None = Field(default=None, max_length=50)

    @field_validator("name", "code", "status")
    @classmethod
    def normalize_optional_value(cls, value: str | None) -> str | None:
        """Trim string fields when provided."""

        return value.strip() if value else value


class CategoryResponse(BaseModel):
    """Asset category payload returned to clients."""

    id: UUID
    name: str
    code: str
    description: str | None = None
    default_warranty_months: int
    is_bookable: bool
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
