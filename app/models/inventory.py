
from sqlalchemy import Column, Integer, Float, String, Date, DATETIME, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base


class Inventory(Base):
    __tablename__ = "inventorys"

    inventory_id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(Integer, ForeignKey("restaurantdescriptions.restaurant_id"),
                           nullable=False
                           )

    menu_id = Column(
        Integer,
        ForeignKey("menu.menu_id"),
        nullable=False
    )

    quantity_available = Column(Integer)

    unit = Column(String(30))

    stock_status = Column(String(30))

    reorder_level = Column(DECIMAL(10, 2))

    last_updated = Column(DATETIME)

    supplier = Column(String(50))


# Relationships
    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="inventory_items"
    )
    menu = relationship(
        "Menu",
        back_populates="inventory_items"
    )
