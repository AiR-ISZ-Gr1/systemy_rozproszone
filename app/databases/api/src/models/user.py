from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    is_admin: bool

    address_id: int | None = Field(default=None, foreign_key="address.id")


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    is_admin: bool | None = None
