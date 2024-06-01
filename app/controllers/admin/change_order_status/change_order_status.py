from fastapi import FastAPI, HTTPException
from typing import List
from config import Order
import requests


app = FastAPI()
api_url = "http://api:8000"


# get all orders with given status
@app.get("/orders", response_model=List[Order])
def get_orders(status):
    response = requests.get(f'{api_url}/orders')
    if not response.status_code == 200:
        raise HTTPException(status_code=response.status_code, detail='ERROR')
    orders = [Order(**order) for order in response.json()]
    if status == 'all':
        return [order for order in orders]
    else:
        return [order for order in orders if order.status == status]


# get order by id
@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    response = requests.get(f'{api_url}/orders/{order_id}')
    if response.status_code == 200:
        return Order(**response.json())
    else:
        raise HTTPException(status_code=404, detail="Order not found")  


# update order status by id and status
@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, status: str):
    order = get_order(order_id)
    order.status = status
    response = requests.put(f"{api_url}/orders/{order_id}", json=order.dict())
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail="Order not found")


# create order
@app.post("/orders", response_model=Order)
def create_order(order: Order):
    # TODO: To implement
    return order


# delete order by id
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    # TODO: To implement
    return None
    