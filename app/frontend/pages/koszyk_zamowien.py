from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests

make_sidebar()
base_url = "http://api:8000"

def change_qunatity(item_id, quantity, product_id):
    delate_product = requests.delete(f"{base_url}/users/{st.session_state.user_id}/cart/items/{item_id}")
    st.write(delate_product)
    #add with new quantity
    add_product = requests.post(f"{base_url}/users/{st.session_state.user_id}/cart/items", 
                                json={"product_id": product_id, "quantity": quantity})




st.write(
    """
# 🛒 KOSZYK ZAMÓWIEŃ

Tutaj znajdziesz wszystkie produkty, które dodałeś do koszyka.
"""
)

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()

for i in get_items_in_cart:
    get_item_name_id = str(i["product_id"])
    choosen_quantity = i["quantity"]
    
    get_item_details = requests.get(f"{base_url}/products/{get_item_name_id}").json()
    get_item_name = get_item_details["name"]
    get_item_price = get_item_details["sell_price"]
    get_accual_quantity = get_item_details["quantity"]
    
    if choosen_quantity > get_accual_quantity:
        change_qunatity(i["id"], get_accual_quantity, get_item_name_id)
        st.experimental_rerun()
        
    
        
    st.subheader(f"**:** {get_item_name}")
    st.write(f"**Cena za sztukę:** {get_item_price} $")
    st.write(f"**Wybrana ilość:** {choosen_quantity}")
    st.write(f"**Dostępna ilość:** {get_accual_quantity}")

    
if st.button("Podsumuj zamówienie"):
    st.switch_page(Links.SEND_PAGE)