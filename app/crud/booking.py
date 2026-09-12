from datetime import date

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate


booking_crud = CRUDBase(Booking)

# ------------------------------------------------------


def get_bookings_by_customer(
    db: Session,
    customer_id: int
):

    return (
        db.query(Booking)
        .filter(
            Booking.customer_id == customer_id
        )
        .all()
    )

# --------------------------------------------------------


def get_bookings_by_date(
    db: Session,
    booking_date: date
):

    return (
        db.query(Booking)
        .filter(
            Booking.booking_date == booking_date
        )
        .all()
    )

# -----------------------------------------------------------


def get_booking_by_table(
    db: Session,
    restaurant_id: int
):

    return (
        db.query(Booking)
        .filter(
            Booking.restaurant_id == restaurant_id
        )
        .all()
    )

# -------------------------------------------------------------


def confirm_booking(
    db: Session,
    booking_id: int
):

    booking = booking_crud.get(
        db,
        booking_id
    )

    if booking:

        booking.booking_status = "Confirmed"

        db.commit()

        db.refresh(booking)

    return booking

# -------------------------------------------------------------


def cancel_booking(
    db: Session,
    booking_id: int
):

    booking = booking_crud.get(
        db,
        booking_id
    )

    if booking:

        booking.booking_status = "Cancelled"

        db.commit()

        db.refresh(booking)

    return booking
# ------------------------------------------------------------------------------------
