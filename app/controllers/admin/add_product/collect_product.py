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
    
    product = Product(
        name = nazwa,
        description = opis,
        sale_price = cena_sprzedazy,
        quantity = ilosc_dostepnych_sztuk,
        buy_price = cena_zakupu,
        date = 'asd',
        picture_path = 'default_path'
    )
    response = requests.post(f"{base_url}/products/", json=product.dict())
    print(response.json())

    return JSONResponse(content={"message": "Produkt został zapisany pomyślnie"}, status_code=200)




# from fastapi import FastAPI, Form, UploadFile, File
# from fastapi.responses import JSONResponse
# import os
# from datetime import datetime
# import shutil

# app = FastAPI()

# @app.post("/products/")
# async def create_product(
#     nazwa: str = Form(...),
#     opis: str = Form(...),
#     cena_sprzedazy: float = Form(...),
#     ilosc_dostepnych_sztuk: int = Form(...),
#     cena_zakupu: float = Form(...),
#     data_wprowadzenia: str = Form(...),
#     zdjecie: UploadFile = File(...)
# ):
#     os.makedirs('products', exist_ok=True)
#     product_id = datetime.now().strftime("%Y%m%d%H%M%S")
#     product_data = {
#         'nazwa': nazwa,
#         'opis': opis,
#         'cena_sprzedazy': cena_sprzedazy,
#         'ilosc_dostepnych_sztuk': ilosc_dostepnych_sztuk,
#         'cena_zakupu': cena_zakupu,
#         'data_wprowadzenia': data_wprowadzenia
#     }

#     # Zapis danych produktu do pliku
#     with open(f'products/{product_id}.txt', 'w') as f:
#         for key, value in product_data.items():
#             f.write(f"{key}: {value}\n")
    
#     # Zapis zdjęcia produktu
#     with open(f'products/{product_id}_{zdjecie.filename}.png', 'wb') as buffer:
#         shutil.copyfileobj(zdjecie.file, buffer)

#     return JSONResponse(content={"message": "Produkt został zapisany pomyślnie"}, status_code=200)

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="127.0.0.1", port=8000)
