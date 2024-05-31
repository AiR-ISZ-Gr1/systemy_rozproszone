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
from PIL import Image
from io import BytesIO

from product import Product, add_product_image, image_download_url, image_upload_url

app = FastAPI()
base_url = "http://api:8000"

@app.post("/products/")
async def create_product(product: Product, img):
    add_product_image(img, product)
    
    response2 = requests.post(f"{base_url}/products/", json=product.dict())
    
    return JSONResponse(content={"message": "Produkt został zapisany pomyślnie"}, status_code=200)
