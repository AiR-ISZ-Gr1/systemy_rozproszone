from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

class Order(BaseModel):
    order_id: int
    order_date: datetime
    customer_id: int
    status: str

# Przykładowe zamówienia
orders = [
    Order(order_id=1, order_date=datetime.now(), customer_id=101, status="new"),
    Order(order_id=2, order_date=datetime.now(), customer_id=102, status="new"),
    Order(order_id=3, order_date=datetime.now(), customer_id=103, status="new"),
    Order(order_id=4, order_date=datetime.now(), customer_id=104, status="new")
]

@app.get("/orders", response_model=List[Order])
def get_orders():
    return orders

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    for order in orders:
        if order.order_id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    orders.append(order)
    return order

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, status: str):
    for order in orders:
        if order.order_id == order_id:
            order.status = status
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for order in orders:
        if order.order_id == order_id:
            orders.remove(order)
            return
    raise HTTPException(status_code=404, detail="Order not found")
