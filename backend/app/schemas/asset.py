"""Asset schemas for AssetFlow inventory management."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.asset import AssetCondition, AssetStatus
from app.schemas.asset_category import CategoryResponse
from app.schemas.auth import UserResponse
from app.schemas.department import DepartmentReference
from app.schemas.common import PaginatedResponse


class AssetBase(BaseModel):
    """Shared asset fields used by create and update payloads."""

    name: str = Field(min_length=2, max_length=150, examples=["Laptop"])
    description: str | None = Field(default=None, max_length=1000)
    category_id: UUID
    department_id: UUID | None = None
    serial_number: str = Field(min_length=2, max_length=100)
    manufacturer: str | None = Field(default=None, max_length=150)
    model_number: str | None = Field(default=None, max_length=150)
    purchase_date: date | None = None
    purchase_cost: Decimal = Field(ge=0, examples=[1200.00])
    warranty_expiry: date | None = None
    condition: AssetCondition = AssetCondition.GOOD
    location: str | None = Field(default=None, max_length=255)
    status: AssetStatus = AssetStatus.AVAILABLE
    is_bookable: bool = False
    photo_url: str | None = Field(default=None, max_length=500)
    document_url: str | None = Field(default=None, max_length=500)

    @field_validator("name", "serial_number", "manufacturer", "model_number", "location", "photo_url", "document_url")
    @classmethod
    def normalize_optional_string(cls, value: str | None) -> str | None:
        """Trim string fields when provided."""

        return value.strip() if value else value

    @field_validator("purchase_cost")
    @classmethod
    def normalize_cost(cls, value: Decimal) -> Decimal:
        """Normalize monetary values to a Decimal instance."""

        return Decimal(value)


class AssetCreate(AssetBase):
    """Payload used to create a new asset."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "description": "Dell Latitude for finance team",
                "category_id": "00000000-0000-0000-0000-000000000001",
                "department_id": "00000000-0000-0000-0000-000000000002",
                "serial_number": "SN-00112233",
                "manufacturer": "Dell",
                "model_number": "Latitude 5440",
                "purchase_date": "2026-01-15",
                "purchase_cost": 1200.0,
                "warranty_expiry": "2027-01-15",
                "condition": "Good",
                "location": "Head Office - Floor 2",
                "status": "Available",
                "is_bookable": False,
                "photo_url": "/uploads/assets/laptop-1.png",
                "document_url": "/uploads/assets/laptop-1.pdf",
            }
        }
    )


class AssetUpdate(BaseModel):
    """Payload used to update an existing asset."""

    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    category_id: UUID | None = None
    department_id: UUID | None = None
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    manufacturer: str | None = Field(default=None, max_length=150)
    model_number: str | None = Field(default=None, max_length=150)
    purchase_date: date | None = None
    purchase_cost: Decimal | None = Field(default=None, ge=0)
    warranty_expiry: date | None = None
    condition: AssetCondition | None = None
    location: str | None = Field(default=None, max_length=255)
    status: AssetStatus | None = None
    is_bookable: bool | None = None
    photo_url: str | None = Field(default=None, max_length=500)
    document_url: str | None = Field(default=None, max_length=500)

    @field_validator("name", "serial_number", "manufacturer", "model_number", "location", "photo_url", "document_url")
    @classmethod
    def normalize_optional_string(cls, value: str | None) -> str | None:
        """Trim string fields when provided."""

        return value.strip() if value else value


class AssetResponse(BaseModel):
    """Asset payload returned to clients."""

    id: UUID
    asset_tag: str
    name: str
    description: str | None = None
    category_id: UUID
    category: CategoryResponse
    department_id: UUID | None = None
    department: DepartmentReference | None = None
    serial_number: str
    manufacturer: str | None = None
    model_number: str | None = None
    purchase_date: date | None = None
    purchase_cost: Decimal
    warranty_expiry: date | None = None
    condition: AssetCondition
    location: str | None = None
    status: AssetStatus
    is_bookable: bool
    photo_url: str | None = None
    document_url: str | None = None
    created_by: UUID | None = None
    created_by_user: UserResponse | None = None
    updated_by: UUID | None = None
    updated_by_user: UserResponse | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetListResponse(PaginatedResponse[AssetResponse]):
    """Paginated list of assets."""


class AssetSearchResponse(PaginatedResponse[AssetResponse]):
    """Paginated asset search response."""
