
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    BigInteger
)
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # Telegram Details
    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String(100),
        nullable=True
    )

    # Personal Details
    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=True
    )

    phone = Column(
        String(15),
        unique=True,
        nullable=True
    )

    email = Column(
        String(100),
        nullable=True
    )

    gender = Column(
        String(10),
        nullable=True
    )

    date_of_birth = Column(
        Date,
        nullable=True
    )

    # Preferences (optional)
    favourite_cuisine = Column(
        String(200),
        nullable=True
    )

    spice_preference = Column(
        String(50),
        nullable=True
    )

    dietary_preference = Column(
        String(50),
        nullable=True
    )

    preferred_table_type = Column(
        String(30),
        nullable=True
    )

    # Statistics
    total_orders = Column(
        Integer,
        default=0
    )

    total_members = Column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at = Column(
        Date,
        nullable=False
    )

    # Relationships
    bookings = relationship(
        "Booking",
        back_populates="customer"
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )

    addresses = relationship(
        "Address",
        back_populates="customer"
    )

    reviews = relationship(
        "Review",
        back_populates="customer"
    )

    favourites = relationship(
        "CustomerFavourite",
        back_populates="customer"
    )

    histories = relationship(
        "UserHistory",
        back_populates="customer"
    )

    conversations = relationship(
        "ChatBotConversation",
        back_populates="customer"
    )

    sessions = relationship(
        "ChatBotSession",
        back_populates="customer"
    )
# from sqlalchemy import Column, Integer, Float, String, Date, DATETIME, INT
# from sqlalchemy.orm import relationship

# from app.database import Base


# class Customer(Base):
#     __tablename__ = "customers"

#     customer_id = Column(Integer, index=True,
#                          primary_key=True, autoincrement=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     phone = Column(String(15), nullable=False, unique=True)
#     email = Column(String(100), nullable=False)
#     gender = Column(String(10), nullable=False)
#     date_of_birth = Column(Date)
#     favourite_cuisine = Column(String(200), nullable=False)
#     spice_preference = Column(String(50), nullable=False)
#     dietary_preference = Column(String(50), nullable=False)
#     preferred_table_type = Column(String(30), nullable=False)
#     total_orders = Column(Integer)
#     created_at = Column(Date, nullable=False)
#     total_memebers = Column(Integer, nullable=False)

# # Relationships
#     bookings = relationship("Booking", back_populates="customer")

#     orders = relationship("Order", back_populates="customer")

#     addresses = relationship("Address", back_populates="customer")

#     reviews = relationship("Review", back_populates="customer")

#     favourites = relationship(
#         "CustomerFavourite",
#         back_populates="customer")

#     histories = relationship(
#         "UserHistory",
#         back_populates="customer"
#     )

#     conversations = relationship(
#         "ChatBotConversation",
#         back_populates="customer"
#     )
