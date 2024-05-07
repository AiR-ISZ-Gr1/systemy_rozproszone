from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import List, Optional


class Cart(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    order_id: int | None = Field(foreign_key="order.id")

    user: Optional["User"] = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[Cart.user_id]"))
    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: str
    quantity: int
    cart_id: int = Field(foreign_key="cart.id")

    cart: Cart = Relationship(back_populates="items")


class CartUpdate(BaseModel):
    user_id: int | None = None
    order_id: int | None = None


class CartItemUpdate(BaseModel):
    product_id: str | None = None
    quantity: int | None = None
