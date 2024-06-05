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

api_callback='http://api:8000'

def restore_product(product: Product):
    product.is_enabled = True
    response = requests.put(f"{api_callback}/products/{product.id}", json=product.dict())
    if response.status_code == 200:
        st.success("Product restored!")

st.write("### Restore Product")

if "restore" not in st.session_state:
    st.session_state["restore"] = False
if "yes" not in st.session_state:
    st.session_state["yes"] = False
if "no" not in st.session_state:
    st.session_state["no"] = False

# if st.button("Button1"):
#     st.session_state["button1"] = not st.session_state["button1"]

name = st.text_input('Product name')
if st.button("Restore Product"):
    # if st.session_state['restore'] == False:
    st.session_state['flower_name'] = name
    st.session_state["restore"] = True
    response = requests.get(f'{api_callback}/products/name/{name}')
    if response.status_code == 200:
        # product = Product(**response.json())
        st.write(f"Are you sure you want to restore {st.session_state['flower_name']} product?")
        if st.button(f"Yes, restore {st.session_state['flower_name']}"):
            st.session_state["yes"] = True
            if st.session_state['restore'] and st.session_state['yes']:
                response = requests.get(f'{api_callback}/products/name/{st.session_state["flower_name"]}')
                restore_product(Product(**response.json()))
                st.session_state['restore'] = False
                st.session_state['yes'] = False
            
            # st.write('hój')
        st.button("No")
    else:
        st.error("No product of this name in database history!")




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
