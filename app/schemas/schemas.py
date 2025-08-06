from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    category_id: int
    brand_id: int
    price: float
    description: Optional[str]

class ProductCreate(BaseModel):
    name: str
    category_id: int
    brand_id: int
    price: float
    description: Optional[str]