from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests

make_sidebar()
base_url = "http://api:8000"

def change_quantity(item_id, quantity, product_id):
    requests.delete(f"{base_url}/users/{st.session_state.user_id}/cart/items/{item_id}")
    if quantity > 0:
        requests.post(f"{base_url}/users/{st.session_state.user_id}/cart/items", 
                    json={"product_id": product_id, "quantity": quantity})
    st.experimental_rerun()

st.write("# 🛒 KOSZYK ZAMÓWIEŃ")

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()


if type(get_items_in_cart) == list and len(get_items_in_cart) > 0:
    # Headers for the table
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])

    col1.subheader("Nazwa produktu")
    col2.subheader("Cena za sztukę")
    col3.subheader("Ilość")
    col4.subheader("Podsumowanie")
    col5.subheader("")

    total_cost = 0

    for i in get_items_in_cart:
        item_id = i["id"]
        product_id = str(i["product_id"])
        chosen_quantity = i["quantity"]
        
        get_item_details = requests.get(f"{base_url}/products/{product_id}").json()
        item_name = get_item_details["name"]
        item_price = get_item_details["sell_price"]
        actual_quantity = get_item_details["quantity"]
        
        if chosen_quantity > actual_quantity:
            change_quantity(item_id, actual_quantity, product_id)
        
        item_total_cost = item_price * chosen_quantity
        total_cost += item_total_cost
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        
        with col1:
            st.write(f"{item_name}")
        with col2:
            st.write(f"{item_price} $/szt.")
        with col3:
            new_quantity = st.number_input("", min_value=0, max_value=actual_quantity, value=chosen_quantity, step=1, key=f"quantity_{item_id}")
        with col4:
            st.write(f"{item_total_cost:.2f} $")
        with col5:
            if new_quantity != chosen_quantity:
                if st.button("Aktualizuj", key=f"update_{item_id}"):
                    change_quantity(item_id, new_quantity, product_id)

    st.write(f"**Całkowity koszt:** {total_cost:.2f} $")

    if st.button("Podsumuj zamówienie"):
        st.switch_page(Links.SEND_PAGE)
else:
    st.write("Twój koszyk jest pusty.")