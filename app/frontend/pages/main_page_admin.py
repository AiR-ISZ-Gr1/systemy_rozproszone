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
from front_objects.classes.product import Product
make_sidebar()


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

api_callback='http://api:8000'

if st.button('Dodaj produkt'):
    if name and description and sell_price and quantity and buy_price and tags and image:
        product = Product(
            name = name,
            description = description,
            sell_price = sell_price,
            quantity = quantity,
            buy_price = buy_price,
            tags = tags
        )
        response = requests.get(f'{api_callback}/products/name/{product.name}')
        if response.status_code == 200:
            st.error('Taka nazwa produktu już istnieje!')
        else:
            product.add_product_image(image)

            # Wysłanie danych do FastAPI
            
            response = requests.post(f'{api_callback}/products/', json=product.dict())

            if response.status_code == 200:
                st.success('Produkt został dodany pomyślnie!')
            else:
                st.error('Wystąpił błąd podczas dodawania produktu.')
    else:
        st.warning('Proszę wypełnić wszystkie pola.')
