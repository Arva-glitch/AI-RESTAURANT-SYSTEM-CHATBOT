from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from decimal import Decimal


class OfferBase(BaseModel):
    restaurant_description_id: int
    offer_name: str
    description: Optional[str] = None
    discount_percentage: Decimal
    start_date: date
    end_date: date


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    offer_name: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class OfferResponse(OfferBase):
    offer_id: int

    model_config = ConfigDict(from_attributes=True)
