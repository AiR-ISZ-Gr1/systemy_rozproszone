import streamlit as st
import requests

from front_objects.navigation import make_sidebar
from front_objects.utils import Links

make_sidebar()

def get_order_history(username):
    try:
        response = requests.get(f"http://history_orders:8007/orders/{username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

def display_order_details(order):
    st.write("### Szczegóły zamówienia")
    st.write(f"**ID Zamówienia:** {order['order_id']}")
    st.write(f"**Produkt:** {order['product']}")
    st.write(f"**Cena:** ${order['price']}")
    st.write(f"**Status:** {order['status']}")

st.title("Historia twoich zamówień")

username = st.session_state.username

if username:
    orders = get_order_history(username)
    if orders:
        for order in orders:
            if st.button(f"Zamówienie #{order['order_id']} ${order['price']}"):
                display_order_details(order)
