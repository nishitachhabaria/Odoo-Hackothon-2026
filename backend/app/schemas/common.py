"""Shared schema primitives for AssetFlow APIs."""

from __future__ import annotations

from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataType = TypeVar("DataType")


class PaginationMeta(BaseModel):
    """Metadata for paginated API responses."""

    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class PaginatedResponse(BaseModel, Generic[DataType]):
    """Standard paginated response envelope."""

    items: list[DataType]
    pagination: PaginationMeta

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_total(
        cls,
        items: list[DataType],
        page: int,
        page_size: int,
        total: int,
    ) -> "PaginatedResponse[DataType]":
        """Build a paginated response from total count and items."""

        return cls(
            items=items,
            pagination=PaginationMeta(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=ceil(total / page_size) if total else 0,
            ),
        )
