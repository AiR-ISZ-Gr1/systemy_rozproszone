from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    street: str
    city: str
    state: str
    country: str

    user: Optional["User"] = Relationship(back_populates="address")


class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
