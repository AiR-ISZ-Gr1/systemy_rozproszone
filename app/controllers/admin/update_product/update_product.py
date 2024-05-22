from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str

products_db = [
    {"id": 1, "name": "Product 1", "description": "Description 1", "price": 10.0, "image_url": "url1"},
    {"id": 2, "name": "Product 2", "description": "Description 2", "price": 20.0, "image_url": "url2"}
]

@app.get("/products", response_model=List[Product])
def get_products():
    return products_db

@app.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/product/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    product_index = next((index for index, product in enumerate(products_db) if product["id"] == product_id), None)
    if product_index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_index] = updated_product.dict()
    return updated_product

