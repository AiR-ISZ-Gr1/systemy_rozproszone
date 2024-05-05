import nanoid
from typing import List
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    price: float
    quantity: int = 0
    description: str = ""
    category: str
    tags: List[str] = []


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None
    category: str | None = None
    tags: List[str] | None = None
