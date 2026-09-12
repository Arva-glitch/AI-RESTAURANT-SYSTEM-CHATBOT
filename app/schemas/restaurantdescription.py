from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import time
from typing import Optional


class RestaurantDescriptionBase(BaseModel):
    restaurant_name: str
    phone_number: str
    email: EmailStr
    cuisine_type: str
    opening_time: time
    closing_time: time
    gst_number: Optional[str] = None
    description: Optional[str] = None


class RestaurantDescriptionCreate(RestaurantDescriptionBase):
    pass


class RestaurantDescriptionUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    cuisine_type: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None


class RestaurantDescriptionResponse(RestaurantDescriptionBase):
    restaurant_description_id: int

    model_config = ConfigDict(from_attributes=True)
