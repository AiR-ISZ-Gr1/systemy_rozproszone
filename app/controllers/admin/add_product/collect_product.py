from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import shutil
from pathlib import Path

import nanoid
from typing import List
from pydantic import BaseModel, Field
import requests

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sale_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str
    picture_path: str

app = FastAPI()
base_url = "http://api:8000"
photos_url = "http://api:8000/files/upload"

@app.post("/products/")
async def create_product(
    nazwa: str = Form(...),
    opis: str = Form(...),
    cena_sprzedazy: float = Form(...),
    ilosc_dostepnych_sztuk: int = Form(...),
    cena_zakupu: float = Form(...),
    data_wprowadzenia: str = Form(...),
    zdjecie: UploadFile = File(...)
): 
    files = {'file': zdjecie.file}
    response1 = requests.post(photos_url, files=files)
    # print(response1.json()['file_id'])
    product = Product(
        name = nazwa,
        description = opis,
        sale_price = cena_sprzedazy,
        quantity = ilosc_dostepnych_sztuk,
        buy_price = cena_zakupu,
        date = 'up to dane',
        picture_path = response1.json()['file_id']
    )
    
    response2 = requests.post(f"{base_url}/products/", json=product.dict())
    

    return JSONResponse(content={"message": "Produkt został zapisany pomyślnie"}, status_code=200)