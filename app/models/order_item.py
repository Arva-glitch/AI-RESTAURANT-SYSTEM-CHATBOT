from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class OrderItem(Base):
    __tablename__ = "orderitems"

    order_item_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    menu_id = Column(
        Integer,
        ForeignKey("menu.menu_id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    total_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    notes = Column(String(255))
    item_status = Column(
        Enum('Pending', 'Preparing', 'Ready', 'Served', 'Cancelled'))

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    menu = relationship(
        "Menu",
        back_populates="order_items"
    )
