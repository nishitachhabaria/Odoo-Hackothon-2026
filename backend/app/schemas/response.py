"""Reusable API response envelope for AssetFlow."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

DataType = TypeVar("DataType")


class APIResponse(BaseModel, Generic[DataType]):
    """Standard JSON envelope for API responses."""

    success: bool = True
    message: str
    data: DataType | None = None
    errors: list[dict[str, object]] | None = None

    model_config = ConfigDict(from_attributes=True)
