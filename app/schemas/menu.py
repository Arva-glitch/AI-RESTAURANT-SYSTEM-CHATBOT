from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional


class MenuBase(BaseModel):
    restaurant_description_id: int
    category_id: int
    food_name: str
    description: Optional[str] = None
    price: Decimal
    is_veg: bool
    is_available: bool = True
    preparation_time: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    food_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_veg: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = None


class MenuResponse(MenuBase):
    menu_id: int

    model_config = ConfigDict(from_attributes=True)
