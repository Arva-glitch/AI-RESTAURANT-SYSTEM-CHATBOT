from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime
from typing import Optional
from app.schemas.enums import BookingStatus


class BookingBase(BaseModel):
    customer_id: int
    restaurant_id: int          # Dining Table ID
    booking_date: date
    booking_time: time
    number_of_guests: int
    booking_status: BookingStatus = BookingStatus.pending

    special_request: Optional[str] = None


class BookingCreate(BookingBase):
    table_id: int | None = None

    booking_status: BookingStatus = BookingStatus.pending

    occasion: str | None = None

    booking_source: str | None = None


class BookingUpdate(BaseModel):
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    number_of_guests: Optional[int] = None
    booking_status: Optional[str] = None
    special_request: Optional[str] = None


class BookingResponse(BookingBase):
    booking_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
