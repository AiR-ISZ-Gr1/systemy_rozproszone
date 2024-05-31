from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
import requests
import logging
from typing import Optional

app = FastAPI()


class OrderDb(BaseModel):
    cart_id: int
    user_id: int
    address_id: int
    date: str = Field(
        default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float


class Address(BaseModel):
    id: Optional[int] = None
    name: str
    street: str
    city: str
    postal_code: str


class Order(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    postal_code: str
    email: str
    payment_method: str
    order_summary: list  # Changed from dict to list
    user_id: int


@app.post("/submit_order/")
async def submit_order(order: Order):
    address = Address(
        name=f"{order.first_name} {order.last_name}",
        street=order.address,
        city=order.city,
        postal_code=order.postal_code,
    )
    response = requests.post("http://api:8000/addresses",
                             json=address.model_dump()).json()
    address_id = response.id

    response = requests.post(f"http://api:8000/users/{order.user_id}").json()
    cart_id = response.cart_id

    dborder = OrderDb(
        status="placed",
        total_amount=420,
        address_id=address_id,
        user_id=order.user_id,
        cart_id=cart_id,
    )
    response = requests.get("http://api:8000/orders",
                            json=dborder.model_dump()).json()

    return dict(message="OK")


@ app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    logging.error(f"Validation error: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
