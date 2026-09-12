from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import Field


class ReviewBase(BaseModel):
    customer_id: int

    restaurant_description_id: int

    order_id: int

    rating: int = Field(
        ge=1,
        le=5,
        description="Rating between 1 and 5"
    )

    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    review_text: Optional[str] = None


class ReviewResponse(ReviewBase):
    review_id: int

    review_date: datetime

    model_config = ConfigDict(from_attributes=True)
