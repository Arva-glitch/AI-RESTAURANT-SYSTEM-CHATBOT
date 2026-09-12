from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class BillBase(BaseModel):
    order_id: int

    subtotal: Decimal

    tax_amount: Decimal

    discount_amount: Decimal = Decimal("0.00")

    total_amount: Decimal

    bill_status: str = "Generated"


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    bill_status: Optional[str] = None


class BillResponse(BillBase):
    bill_id: int

    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
