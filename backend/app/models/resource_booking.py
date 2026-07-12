"""Resource booking ORM model for AssetFlow."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BookingStatus(str, Enum):
    """Supported resource booking statuses."""

    UPCOMING = "Upcoming"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ResourceBooking(Base):
    """Resource booking record."""

    __tablename__ = "resource_bookings"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    asset_id: Mapped[UUID] = mapped_column(ForeignKey("assets.id"), nullable=False, index=True)
    booked_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    department_id: Mapped[UUID | None] = mapped_column(ForeignKey("departments.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(SAEnum(BookingStatus, name="booking_status"), nullable=False, default=BookingStatus.UPCOMING, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    asset: Mapped["Asset"] = relationship("Asset")
    booked_by_user: Mapped["User"] = relationship("User")
    department: Mapped["Department | None"] = relationship("Department")
