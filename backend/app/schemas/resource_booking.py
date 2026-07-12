"""Resource booking schemas for AssetFlow."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, root_validator


class BookingCreate(BaseModel):
    asset_id: UUID
    title: str = Field(min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    start_datetime: datetime
    end_datetime: datetime

    @root_validator(skip_on_failure=True)
    def validate_datetimes(cls, values: dict[str, object]) -> dict[str, object]:
        start_datetime = values.get("start_datetime")
        end_datetime = values.get("end_datetime")
        if start_datetime is not None and end_datetime is not None and start_datetime >= end_datetime:
            raise ValueError("start_datetime must be before end_datetime")
        return values


class BookingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    status: str | None = None

    @root_validator(skip_on_failure=True)
    def validate_datetimes(cls, values: dict[str, object]) -> dict[str, object]:
        start_datetime = values.get("start_datetime")
        end_datetime = values.get("end_datetime")
        if start_datetime is not None and end_datetime is not None and start_datetime >= end_datetime:
            raise ValueError("start_datetime must be before end_datetime")
        return values


class BookingResponse(BaseModel):
    id: UUID
    asset_id: UUID
    booked_by: UUID
    department_id: UUID | None = None
    title: str
    description: str | None = None
    start_datetime: datetime
    end_datetime: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingCalendarResponse(BaseModel):
    id: UUID
    title: str
    start_datetime: datetime
    end_datetime: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
