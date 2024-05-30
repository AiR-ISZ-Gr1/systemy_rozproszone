from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests

make_sidebar()
base_url = "http://api:8000"

def change_quantity(item_id, quantity, product_id):
    requests.delete(f"{base_url}/users/{st.session_state.user_id}/cart/items/{item_id}")
    requests.post(f"{base_url}/users/{st.session_state.user_id}/cart/items", 
                  json={"product_id": product_id, "quantity": quantity})
    st.experimental_rerun()

st.write("# 🛒 KOSZYK ZAMÓWIEŃ")

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()

col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

col1.subheader("Product name")
col2.subheader("Priece per item")
col3.subheader("Number of items")
col4.subheader("All price")

for i in get_items_in_cart:
    item_id = i["id"]
    product_id = str(i["product_id"])
    choosen_quantity = i["quantity"]
    
    get_item_details = requests.get(f"{base_url}/products/{product_id}").json()
    item_name = get_item_details["name"]
    item_price = get_item_details["sell_price"]
    actual_quantity = get_item_details["quantity"]
    
    if choosen_quantity > actual_quantity:
        change_quantity(item_id, actual_quantity, product_id)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
       
    with col1:
        st.write(f"**{item_name}**")
    with col2:
        st.write(f"{item_price} $/szt.")
    with col3:
        new_quantity = st.number_input("", min_value=1, max_value=actual_quantity, value=choosen_quantity, step=1, key=f"quantity_{item_id}")
    with col4:
        if new_quantity != choosen_quantity:
            if st.button("Aktualizuj", key=f"update_{item_id}"):
                change_quantity(item_id, new_quantity, product_id)

if st.button("Podsumuj zamówienie"):
    st.switch_page(Links.SEND_PAGE)
