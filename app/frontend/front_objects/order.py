from sqlmodel import SQLModel, Field
# from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    address_id: int = Field(foreign_key="address.id")
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float
