from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from config import Order
import requests

app = FastAPI()
api_url = "http://api:8000"


@app.get("/orders", response_model=List[Order])
def get_orders():
    response = requests.get(f'{api_url}/orders')
    return [Order(**order) for order in response.json()]

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
