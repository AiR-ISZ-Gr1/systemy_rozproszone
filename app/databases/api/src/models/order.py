from sqlmodel import SQLModel, Field
from enum import Enum


class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    date: str
    status: str
    total_amount: float


class OrderStatus(str, Enum):
    PLACED = "placed"
    DONE = "done"
