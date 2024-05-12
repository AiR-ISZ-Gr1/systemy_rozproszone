from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import BaseModel


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    date: str
    status: str
    total_amount: float


class OrderStatus(str, Enum):
    PLACED = "placed"
    DONE = "done"


class OrderUpdate(BaseModel):
    cart_id: int | None = None
    user_id: int | None = None
    date: str | None = None
    status: str | None = None
    total_amount: float | None = None
