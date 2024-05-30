import streamlit as st
import requests
from datetime import datetime
from pydantic import BaseModel, Field
import nanoid
from typing import List
from fastapi import UploadFile
from PIL import Image
from io import BytesIO
# from app.databases.api.src.models.product import Product
from front_objects.navigation_admin import make_sidebar
make_sidebar()

image_upload_url = "http://api:8000/files/upload"
class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)

# Function to compress image
def compress_image(img: Image.Image, output_size=(320, 320), quality=70) -> BytesIO:
    img.thumbnail(output_size)
    output = BytesIO()
    img.save(output, format='PNG', quality=quality)
    output.seek(0)
    return output

# Function to add product image
def add_product_image(file, product: Product):
    img = compress_image(Image.open(file))
    img_extension = file.name.split('.')[-1]
    files = {'file': (f'{product.date}_{product.name}.{img_extension}', img, f'image/{img_extension}')}
    response = requests.post(image_upload_url, files=files)
    response.raise_for_status()  # Check for request errors
    product.image_id = response.json().get('file_id')
    return response


st.title('Add new Product')

name = st.text_input('Name')
description = st.text_area('Description')
sell_price = st.number_input('Sell price', min_value=0.0, format="%.2f")
quantity = st.number_input('Avaliable quantity', min_value=0)
buy_price = st.number_input('Buy price', min_value=0.0, format="%.2f")
tags = st.multiselect(
    "Categories",
    ["Flower", "Tree", "Object", "Other", "Manure"],
    ["Flower"])
image = st.file_uploader('Photo of the product', type=['jpg', 'jpeg', 'png'])


if st.button('Dodaj produkt'):
    if name and description and sell_price and quantity and buy_price and tags:
        # Przygotowanie danych do wysłania
        # st.write("tags:", tags[0])
        # file = {'image': image.getvalue()}
        product = Product(
            name = name,
            description = description,
            sell_price = sell_price,
            quantity = quantity,
            buy_price = buy_price,
            tags = tags
        )

        add_product_image(image, product)

        # Wysłanie danych do FastAPI
        api_callback='http://api:8000'
        response = requests.post(f'{api_callback}/products/', json=product.dict())

        if response.status_code == 200:
            st.success('Produkt został dodany pomyślnie!')
        else:
            st.error('Wystąpił błąd podczas dodawania produktu.')
    else:
        st.warning('Proszę wypełnić wszystkie pola.')