from sqlalchemy import (
    Column,
    Integer,
    Date,
    Time,
    String,
    ForeignKey,
    DateTime,
    Enum
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    table_id = Column(
        Integer,
        ForeignKey("diningtables.table_id"),
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurantdescriptions.restaurant_id"),
        nullable=False
    )

    booking_date = Column(Date, nullable=False)

    booking_time = Column(Time, nullable=False)

    number_of_guests = Column(Integer, nullable=False)

    booking_status = Column(String(30), default="Pending")

    special_request = Column(String(255))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    occassion = Column(Enum("Casual", "Birthday", "Anniversary"))
    booking_source = Column(Enum("Swiggy", "Zomato"))

    customer = relationship(
        "Customer",
        back_populates="bookings"
    )

    table = relationship(
        "Diningtable",
        back_populates="bookings"
    )

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="bookings"
    )

    orders = relationship(
        "Order",
        back_populates="booking"
    )
