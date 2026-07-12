"""Resource booking service for AssetFlow."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import ResourceBooking
from app.repositories.booking_repository import BookingRepository
from app.schemas.resource_booking import BookingCreate, BookingResponse, BookingUpdate


class BookingService:
    """Business rules for resource bookings."""

    def __init__(self, booking_repository: BookingRepository, session: Session) -> None:
        self.booking_repository = booking_repository
        self.session = session

    def create_booking(self, payload: BookingCreate, user_id: UUID, department_id: UUID | None) -> BookingResponse:
        self._validate_asset(payload.asset_id)
        self._validate_booking_times(payload.start_datetime, payload.end_datetime)
        self._validate_no_overlap(payload.asset_id, payload.start_datetime, payload.end_datetime)

        booking = self.booking_repository.create_booking_record(
            asset_id=payload.asset_id,
            booked_by=user_id,
            department_id=department_id,
            title=payload.title,
            description=payload.description,
            start_datetime=payload.start_datetime,
            end_datetime=payload.end_datetime,
            status=self._resolve_status(payload.start_datetime, payload.end_datetime),
        )
        return BookingResponse.model_validate(booking)

    def update_booking(self, booking_id: UUID, payload: BookingUpdate) -> BookingResponse:
        booking = self._get_existing_booking(booking_id)
        update_data: dict[str, Any] = {}

        if payload.title is not None:
            update_data["title"] = payload.title
        if payload.description is not None:
            update_data["description"] = payload.description
        if payload.start_datetime is not None:
            update_data["start_datetime"] = payload.start_datetime
        if payload.end_datetime is not None:
            update_data["end_datetime"] = payload.end_datetime
        if payload.status is not None:
            update_data["status"] = payload.status

        if "start_datetime" in update_data or "end_datetime" in update_data:
            start_datetime = update_data.get("start_datetime", booking.start_datetime)
            end_datetime = update_data.get("end_datetime", booking.end_datetime)
            self._validate_booking_times(start_datetime, end_datetime)
            self._validate_no_overlap(booking.asset_id, start_datetime, end_datetime, exclude_booking_id=booking.id)
            update_data["status"] = self._resolve_status(start_datetime, end_datetime)

        booking = self.booking_repository.update_booking(booking, update_data)
        return BookingResponse.model_validate(booking)

    def cancel_booking(self, booking_id: UUID) -> BookingResponse:
        booking = self._get_existing_booking(booking_id)
        if booking.status == "Cancelled":
            return BookingResponse.model_validate(booking)
        booking = self.booking_repository.cancel_booking(booking)
        return BookingResponse.model_validate(booking)

    def list_bookings(self, limit: int = 100, offset: int = 0) -> list[BookingResponse]:
        bookings = self.booking_repository.list_bookings(limit=limit, offset=offset)
        return [BookingResponse.model_validate(booking) for booking in bookings]

    def get_booking(self, booking_id: UUID) -> BookingResponse:
        booking = self._get_existing_booking(booking_id)
        return BookingResponse.model_validate(booking)

    def get_calendar(self, asset_id: UUID) -> list[BookingResponse]:
        if not self.booking_repository.asset_exists(asset_id):
            raise ValueError("Asset does not exist")
        bookings = self.booking_repository.get_calendar(asset_id)
        return [BookingResponse.model_validate(booking) for booking in bookings]

    def _get_existing_booking(self, booking_id: UUID) -> ResourceBooking:
        booking = self.booking_repository.get_booking(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        return booking

    def _resolve_status(self, start_datetime: datetime, end_datetime: datetime) -> str:
        now = datetime.utcnow()
        if now < start_datetime:
            return "Upcoming"
        if now >= start_datetime and now < end_datetime:
            return "Ongoing"
        return "Completed"

    def _validate_asset(self, asset_id: UUID) -> None:
        if not self.booking_repository.asset_exists(asset_id):
            raise ValueError("Asset does not exist")
        if not self.booking_repository.is_asset_bookable(asset_id):
            raise ValueError("Asset is not bookable")

    def _validate_booking_times(self, start_datetime: datetime, end_datetime: datetime) -> None:
        if start_datetime >= end_datetime:
            raise ValueError("start_datetime must be before end_datetime")

    def _validate_no_overlap(self, asset_id: UUID, start_datetime: datetime, end_datetime: datetime, exclude_booking_id: UUID | None = None) -> None:
        overlapping = self.booking_repository.get_bookings_for_asset(asset_id, start_datetime, end_datetime, exclude_booking_id=exclude_booking_id)
        if overlapping:
            raise ValueError("Booking overlaps with an existing reservation")
