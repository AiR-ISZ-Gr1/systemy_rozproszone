from fastapi import FastAPI, HTTPException
from typing import List
import requests

from config import Product


app = FastAPI()
api_url = "http://api:8000"


@app.get("/products/", response_model=List[Product])
def get_products():
    response = requests.get(f'{api_url}/products')
    # product = Product(**response.json())
    return response.json()

@app.get("/products/low_stock/", response_model=List[Product])
def get_low_stock_products():
    products = get_products()

    return products.json() # [product for product in products if product['quantity'] < 20]

@app.post("/products/", response_model=Product)
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product_stock(product_id: int, additional_stock: int):
    for product in products:
        if product.id == product_id:
            product.stock += additional_stock
            return product
    raise HTTPException(status_code=404, detail="Product not found")
