from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CustomerFavouriteBase(BaseModel):
    customer_id: int
    menu_id: int


class CustomerFavouriteCreate(CustomerFavouriteBase):
    pass


class CustomerFavouriteUpdate(BaseModel):
    menu_id: int


class CustomerFavouriteResponse(CustomerFavouriteBase):
    favourite_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
