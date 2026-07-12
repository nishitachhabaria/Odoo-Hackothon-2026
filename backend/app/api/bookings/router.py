"""Bookings API router for AssetFlow."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.bookings.repository import BookingRepository
from app.api.bookings.schema import APIResponse, BookingCalendarResponse, BookingCreate, BookingResponse, BookingUpdate
from app.api.bookings.service import BookingService
from app.database.session import get_db
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/api/v1/bookings", tags=["Bookings"])


def get_booking_service(db: Session = Depends(get_db)) -> BookingService:
    """Create booking service for the current request."""

    return BookingService(BookingRepository(db), db)


@router.post("", response_model=APIResponse[BookingResponse], status_code=201)
def create_booking(
    payload: BookingCreate,
    current_user=Depends(get_current_active_user),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[BookingResponse]:
    try:
        data = service.create_booking(payload, current_user.id, current_user.department_id)
    except ValueError as exc:
        raise HTTPException(status_code=409 if "overlaps" in str(exc).lower() else 400, detail=str(exc))
    return APIResponse(message="Booking created successfully", data=data)


@router.get("", response_model=APIResponse[list[BookingResponse]])
def list_bookings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[list[BookingResponse]]:
    offset = (page - 1) * page_size
    data = service.list_bookings(limit=page_size, offset=offset)
    return APIResponse(message="Bookings retrieved successfully", data=data)


@router.get("/{booking_id}", response_model=APIResponse[BookingResponse])
def get_booking(
    booking_id: UUID = Path(...),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[BookingResponse]:
    try:
        data = service.get_booking(booking_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return APIResponse(message="Booking retrieved successfully", data=data)


@router.put("/{booking_id}", response_model=APIResponse[BookingResponse])
def update_booking(
    booking_id: UUID = Path(...),
    payload: BookingUpdate = Depends(),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[BookingResponse]:
    try:
        data = service.update_booking(booking_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400 if "overlaps" not in str(exc).lower() else 409, detail=str(exc))
    return APIResponse(message="Booking updated successfully", data=data)


@router.delete("/{booking_id}", response_model=APIResponse[dict[str, str]])
def cancel_booking(
    booking_id: UUID = Path(...),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[dict[str, str]]:
    try:
        service.cancel_booking(booking_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return APIResponse(message="Booking cancelled successfully", data={"status": "cancelled"})


@router.get("/calendar/{asset_id}", response_model=APIResponse[list[BookingCalendarResponse]])
def booking_calendar(
    asset_id: UUID = Path(...),
    service: BookingService = Depends(get_booking_service),
) -> APIResponse[list[BookingCalendarResponse]]:
    try:
        bookings = service.get_calendar(asset_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    calendar = [BookingCalendarResponse.model_validate(booking) for booking in bookings]
    return APIResponse(message="Booking calendar retrieved successfully", data=calendar)
