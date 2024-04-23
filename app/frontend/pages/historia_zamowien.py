import streamlit as st

from front_objects.navigation import make_sidebar
from front_objects.utils import Links

make_sidebar()

orders_database = {
    1: {"order_id": 1, "product": "Laptop", "price": 1500, "status": "Przyjęte"},
    2: {"order_id": 2, "product": "Smartphone", "price": 800, "status": "W trakcie realizacji"},
    3: {"order_id": 3, "product": "Słuchawki", "price": 200, "status": "Dostarczone"},
}

def display_order_details(order):
    st.write("### Szczegóły zamówienia")
    st.write(f"**ID Zamówienia:** {order['order_id']}")
    st.write(f"**Produkt:** {order['product']}")
    st.write(f"**Cena:** ${order['price']}")
    st.write(f"**Status:** {order['status']}")

st.title("Historia twoich zamówień")
for order_id, order in orders_database.items():
    if st.button(f"Zamówienie #{order_id} ${order['price']}"):
        display_order_details(order)