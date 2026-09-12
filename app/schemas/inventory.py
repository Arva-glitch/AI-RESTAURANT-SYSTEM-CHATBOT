from pydantic import BaseModel, ConfigDict
from typing import Optional


class InventoryBase(BaseModel):
    restaurant_description_id: int
    menu_id: int
    quantity_available: int
    unit: str
    stock_status: str


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity_available: Optional[int] = None
    unit: Optional[str] = None
    stock_status: Optional[str] = None


class InventoryResponse(InventoryBase):
    inventory_id: int

    model_config = ConfigDict(from_attributes=True)
