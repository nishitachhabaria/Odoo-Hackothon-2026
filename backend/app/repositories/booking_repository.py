"""Resource booking repository for AssetFlow."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.orm import Session

from app.models import Asset, ResourceBooking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[ResourceBooking]):
    """Repository for resource booking queries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_booking(self, booking_id: UUID) -> ResourceBooking | None:
        statement = select(ResourceBooking).where(ResourceBooking.id == booking_id)
        return self.session.execute(statement).scalar_one_or_none()

    def list_bookings(self, limit: int = 100, offset: int = 0) -> list[ResourceBooking]:
        statement = select(ResourceBooking).order_by(ResourceBooking.start_datetime.asc()).limit(limit).offset(offset)
        return self.session.execute(statement).scalars().all()

    def get_bookings_for_asset(self, asset_id: UUID, start_datetime: datetime, end_datetime: datetime, exclude_booking_id: UUID | None = None) -> list[ResourceBooking]:
        criteria = [ResourceBooking.asset_id == asset_id]
        if exclude_booking_id is not None:
            criteria.append(ResourceBooking.id != exclude_booking_id)

        overlap = and_(
            ResourceBooking.start_datetime < end_datetime,
            ResourceBooking.end_datetime > start_datetime,
            ResourceBooking.status != "Cancelled",
        )

        statement = select(ResourceBooking).where(and_(*criteria, overlap)).order_by(ResourceBooking.start_datetime.asc())
        return self.session.execute(statement).scalars().all()

    def create_booking(self, booking: ResourceBooking) -> ResourceBooking:
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking

    def update_booking(self, booking: ResourceBooking, values: dict[str, Any]) -> ResourceBooking:
        for name, value in values.items():
            setattr(booking, name, value)
        self.session.commit()
        self.session.refresh(booking)
        return booking

    def cancel_booking(self, booking: ResourceBooking) -> ResourceBooking:
        booking.status = "Cancelled"
        self.session.commit()
        self.session.refresh(booking)
        return booking

    def create_booking_record(self, asset_id: UUID, booked_by: UUID, department_id: UUID | None, title: str, description: str | None, start_datetime: datetime, end_datetime: datetime, status: str) -> ResourceBooking:
        booking = ResourceBooking(
            asset_id=asset_id,
            booked_by=booked_by,
            department_id=department_id,
            title=title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            status=status,
        )
        return self.create_booking(booking)

    def get_calendar(self, asset_id: UUID) -> list[ResourceBooking]:
        statement = select(ResourceBooking).where(ResourceBooking.asset_id == asset_id).order_by(ResourceBooking.start_datetime.asc())
        return self.session.execute(statement).scalars().all()

    def asset_exists(self, asset_id: UUID) -> bool:
        statement = select(func.count()).select_from(Asset).where(Asset.id == asset_id)
        return int(self.session.execute(statement).scalar_one()) > 0

    def is_asset_bookable(self, asset_id: UUID) -> bool:
        statement = select(func.count()).select_from(Asset).where(Asset.id == asset_id, Asset.is_bookable.is_(True))
        return int(self.session.execute(statement).scalar_one()) > 0
