from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    DateTime,
    String,
    Enum
)

from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from app.database import Base


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
        unique=True
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    tax_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    discount_amount = Column(
        Numeric(10, 2),
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    bill_status = Column(
        String(30),
        default="Generated"
    )

    generated_at = Column(
        DateTime,
        server_default=func.now()
    )
    service_charges = Column(Integer)

    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))

    table_id = Column(Integer, ForeignKey("diningtables.table_id"))

    order_type = Column(Enum("Dine in", "Dilevery", "Take Away"))

    order_status = Column(
        Enum("Pending", "Preparing", "Ready", "Delivered", "Cancelled"))

    order = relationship(
        "Order",
        back_populates="bill"
    )

    payment = relationship(
        "Payment",
        back_populates="bill",
        uselist=False
    )
