from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    category_id: int

    model_config = ConfigDict(from_attributes=True)
