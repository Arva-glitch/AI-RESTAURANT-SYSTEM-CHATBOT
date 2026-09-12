from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import List, Optional

from app.schemas.enums import OrderType


class OrderItemRequest(BaseModel):
    menu_id: int
    quantity: int = Field(gt=0)


class PlaceOrderRequest(BaseModel):
    customer_id: int

    booking_id: Optional[int] = None

    restaurant_description_id: int

    coupon_id: Optional[int] = None

    order_type: OrderType

    items: List[OrderItemRequest]

    special_instruction: Optional[str] = None


class PlaceOrderResponse(BaseModel):

    order_id: int

    total_items: int

    subtotal: Decimal

    tax: Decimal

    discount: Decimal

    grand_total: Decimal

    payment_status: str

    message: str

    model_config = ConfigDict(from_attributes=True)


class UpdateOrderItemRequest(BaseModel):
    order_item_id: int

    quantity: Optional[int] = Field(default=None, gt=0)

    remove_item: bool = False
