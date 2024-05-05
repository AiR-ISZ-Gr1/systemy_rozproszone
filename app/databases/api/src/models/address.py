from sqlmodel import SQLModel, Field


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    street: str
    city: str
    state: str
    country: str
