from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional
from app.schemas.enums import ItemStatus


class OrderItemBase(BaseModel):
    order_id: int

    menu_id: int

    quantity: int

    unit_price: Decimal

    total_price: Decimal

    item_status: ItemStatus = ItemStatus.pending

    notes: Optional[str] = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    item_status: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(OrderItemBase):
    order_item_id: int

    model_config = ConfigDict(from_attributes=True)
