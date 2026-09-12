from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Time
from sqlalchemy.orm import relationship
from app.database import Base


class Menu(Base):
    __tablename__ = "menu"

    menu_id = Column(Integer, primary_key=True, index=True)
    restaurant_description_id = Column(
        Integer,
        ForeignKey("restaurantdescriptions.restaurant_id"),
        nullable=False
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )
    food_name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    is_veg = Column(Boolean)
    is_available = Column(Boolean, default=True)
    preparation_time = Column(Time)
    cuisine = Column(String(30), nullable=False)
    food_type = Column(String(50), nullable=False)
    spice_level = Column(String(30))
    serving_size = Column(String(30))
    allergens = Column(String(50))
    chefs_special = Column(String(30), default=False)

    restaurant_description = relationship(
        "Restaurant_Description",
        back_populates="menu_items"
    )

    category = relationship(
        "Category",
        back_populates="menu_items"
    )

    inventory_items = relationship(
        "Inventory",
        back_populates="menu"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="menu"
    )

    favourites = relationship(
        "CustomerFavourite",
        back_populates="menu"
    )
