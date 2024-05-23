from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pandas as pd
import os
import logging

app = FastAPI()

class Order(BaseModel):
    username: str
    first_name: str
    last_name: str
    address: str
    city: str
    postal_code: str
    email: str
    payment_method: str
    order_summary: list  # Changed from dict to list

@app.post("/submit_order/")
async def submit_order(order: Order):
    try:
        file_exists = os.path.isfile('orders.csv')
        df = pd.DataFrame([order.dict()])

        if file_exists:
            df.to_csv('../send_order/orders.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('../send_order/orders.csv', index=False)

        return {"message": "Order received successfully"}
    except Exception as e:
        logging.error(f"Error processing order: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    logging.error(f"Validation error: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
