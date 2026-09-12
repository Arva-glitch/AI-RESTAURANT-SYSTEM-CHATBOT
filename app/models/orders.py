from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Numeric, func
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.booking_id")
    )

    restaurant_description_id = Column(
        Integer,
        ForeignKey(
            "restaurantdescriptions.restaurant_id"
        ),
        nullable=False
    )

    coupon_id = Column(
        Integer,
        ForeignKey("coupons.coupon_id")
    )

    order_type = Column(String(30))

    order_status = Column(String(30))

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    special_instruction = Column(String(255))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    estimated_delivery_time = Column(DateTime)
    special_instruction = Column(String(300))
    order_date = Column(DateTime)

    # Relationship
    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    booking = relationship(
        "Booking",
        back_populates="orders"
    )

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="orders"
    )

    coupon = relationship(
        "Coupon",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order"
    )

    bill = relationship(
        "Bill",
        back_populates="order",
        uselist=False
    )
    review = relationship(
        "Review",
        back_populates="order",
        uselist=False
    )
