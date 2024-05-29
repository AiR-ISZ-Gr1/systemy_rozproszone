import nanoid
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sale_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str
    picture_path: str


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str = "default description"
    sale_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str | None = None
    picture_path: str | None = None


# import nanoid
# from typing import List
# from pydantic import BaseModel, Field


# class Product(BaseModel):
#     id: str = Field(default_factory=lambda: nanoid.generate(size=10))
#     name: str
#     price: float
#     quantity: int = 0
#     description: str = ""
#     category: str
#     tags: List[str] = []


# class ProductUpdate(BaseModel):
#     name: str | None = None
#     price: float | None = None
#     quantity: int | None = None
#     description: str | None = None
#     category: str | None = None
#     tags: List[str] | None = None