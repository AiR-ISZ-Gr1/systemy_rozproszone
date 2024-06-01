from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Order(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    address_id: int = Field(foreign_key="address.id")
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float


class Cart(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    quantity: int
    cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")

    cart: Cart = Relationship(back_populates="items")