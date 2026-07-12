"""Asset ORM model for AssetFlow."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AssetStatus(str, Enum):
    """Supported asset lifecycle statuses."""

    AVAILABLE = "Available"
    ALLOCATED = "Allocated"
    RESERVED = "Reserved"
    UNDER_MAINTENANCE = "Under Maintenance"
    LOST = "Lost"
    RETIRED = "Retired"
    DISPOSED = "Disposed"


class AssetCondition(str, Enum):
    """Supported asset condition states."""

    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    DAMAGED = "Damaged"


class Asset(Base):
    """Asset inventory record."""

    __tablename__ = "assets"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    asset_tag: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("asset_categories.id"), nullable=False, index=True)
    department_id: Mapped[UUID | None] = mapped_column(ForeignKey("departments.id"), nullable=True, index=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    manufacturer: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    model_number: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    purchase_cost: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=Decimal("0"))
    warranty_expiry: Mapped[date | None] = mapped_column(Date, nullable=True)
    condition: Mapped[AssetCondition] = mapped_column(SAEnum(AssetCondition, name="asset_condition"), nullable=False, default=AssetCondition.GOOD)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[AssetStatus] = mapped_column(SAEnum(AssetStatus, name="asset_status"), nullable=False, default=AssetStatus.AVAILABLE, index=True)
    is_bookable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    document_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    updated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    category: Mapped["AssetCategory"] = relationship("AssetCategory")
    department: Mapped["Department | None"] = relationship("Department")
    created_by_user: Mapped["User | None"] = relationship("User", foreign_keys=[created_by])
    updated_by_user: Mapped["User | None"] = relationship("User", foreign_keys=[updated_by])
