from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests

make_sidebar()
base_url = "http://api:8000"

def change_quantity(item_id, quantity, product_id):
    delete_product = requests.delete(f"{base_url}/users/{st.session_state.user_id}/cart/items/{item_id}")
    st.write(delete_product)
    # Add with new quantity
    add_product = requests.post(f"{base_url}/users/{st.session_state.user_id}/cart/items", 
                                json={"product_id": product_id, "quantity": quantity})
    st.experimental_rerun()

st.write(
    """
# 🛒 KOSZYK ZAMÓWIEŃ

Tutaj znajdziesz wszystkie produkty, które dodałeś do koszyka.
"""
)

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()

for i in get_items_in_cart:
    item_id = i["id"]
    product_id = str(i["product_id"])
    choosen_quantity = i["quantity"]
    
    get_item_details = requests.get(f"{base_url}/products/{product_id}").json()
    get_item_name = get_item_details["name"]
    get_item_price = get_item_details["sell_price"]
    get_actual_quantity = get_item_details["quantity"]
    
    if choosen_quantity > get_actual_quantity:
        change_quantity(item_id, get_actual_quantity, product_id)
        st.experimental_rerun()

    st.subheader(f"{get_item_name}")
    st.write(f"**Cena za sztukę:** {get_item_price} $")
    st.write(f"**Wybrana ilość:** {choosen_quantity}")
    st.write(f"**Dostępna ilość:** {get_actual_quantity}")

    new_quantity = st.number_input(f"Zmień ilość dla {get_item_name}", min_value=1, max_value=get_actual_quantity, value=choosen_quantity, step=1, key=f"quantity_{item_id}")
    if new_quantity != choosen_quantity:
        if st.button(f"Zaktualizuj ilość dla {get_item_name}", key=f"update_{item_id}"):
            change_quantity(item_id, new_quantity, product_id)

if st.button("Podsumuj zamówienie"):
    st.switch_page(Links.SEND_PAGE)
