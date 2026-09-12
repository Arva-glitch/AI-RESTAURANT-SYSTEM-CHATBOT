
from sqlalchemy import Column, Integer, Float, String, Date, DATETIME, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Restaurant_Description(Base):
    __tablename__ = "restaurantdescriptions"

    restaurant_id = Column(Integer, primary_key=True,
                           index=True, autoincrement=True)
    restaurant_name = Column(String(100), nullable=False)
    restaurant_address = Column(String(300), nullable=False)
    restaurant_landmark = Column(String(300))
    restaurant_capacity = Column(Integer)
    phone_number = Column(String(15), nullable=False, unique=True)
    pincode = Column(String(20))
    email = Column(String(100), nullable=False, unique=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    cuisine_type = Column(String(100), nullable=False)
    gst_number = Column(String(30), unique=True)
    restaurant_status = Column(String(20), nullable=False, default="Open")
    average_cost_for_two = Column(Integer, default=2000)

    # Relationships

    menu_items = relationship("Menu", back_populates="restaurant_description")
    staff_members = relationship(
        "Staff", back_populates="restaurant_description")
    inventory_items = relationship(
        "Inventory", back_populates="restaurant_description")
    offers = relationship("Offer", back_populates="restaurant_description")
    bookings = relationship("Booking", back_populates="restaurant_description")
    orders = relationship("Order", back_populates="restaurant_description")
    reviews = relationship("Review", back_populates="restaurant_description")
