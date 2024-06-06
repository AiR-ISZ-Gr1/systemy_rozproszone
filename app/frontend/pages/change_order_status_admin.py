import streamlit as st
import requests
import datetime
from front_objects.navigation_admin import make_sidebar
from front_objects.classes.order import Order, OrderStatus
from front_objects.classes.cart import Cart
from typing import Optional
make_sidebar()

API_URL = "http://change_order_status:8004"

def fetch_orders(order_status: str = 'all'):        
    response = requests.get(f"{API_URL}/orders", params={"order_status": order_status})
    if response.status_code == 200:
        return [Order(**order) for order in response.json()]
    else:
        return []

# def fetch_order_by_id(order_id):
#     response = requests.get(f"{API_URL}/orders/{order_id}")
#     if response.status_code == 200:
#         return Order(**response.json())
#     else:
#         return None

def fetch_order_by_id(order_id: int) -> Optional[Order]:
    response = requests.get(f"{API_URL}/orders/{order_id}")
    if response.status_code == 200:
        return Order(**response.json())
    else:
        return None


def update_order_status(order_id: int, order_status: str):
    url = "http://api:8000"
    order = fetch_order_by_id(order_id)
    order.status = order_status
    response = requests.put(f"{url}/orders/{order_id}", json=order.dict())
    return response.status_code == 200

# def update_order_status(order_id: int, status: OrderStatus):
#     url = "http://api:8000"
#     order = fetch_order_by_id(order_id)
#     order.status = status
#     response = requests.put(f"{url}/orders/{order_id}", params={"status": status})
#     return response.status_code == 200
st.title("Order Management System")

search_id = st.text_input("Enter Order ID to search")

if search_id:
    order = fetch_order_by_id(search_id)
    # st.write(order)r
    if order:
        st.write(f"Order ID: {order.id}")
        st.write(f"Order Date: {order.date}")
        st.write(f"Customer ID: {order.user_id}")
        # st.write(f"df {order.items}")
        st.write(f"Status: {order.status}")
        
        new_status = st.selectbox("Change Status", [status.value for status in OrderStatus], key=order.id)
        if st.button("Update Status", key=f"update_{order.id}"):
            if update_order_status(order.id, new_status):
                st.success(f"Order {order.id} status updated to {new_status}")
            else:
                st.error("Failed to update order status")
    else:
        st.error("Order not found")

# Filter orders by status
st.write("---")
st.header("All Orders")

status_filter = st.selectbox("Filter by Status", [status.value for status in OrderStatus] + ['all'])

# if status_filter == "all":
orders = fetch_orders()
# else:
#     orders = fetch_orders(status=status_filter)

# st.write(f"Displaying {len(orders)} orders with status {status_filter}")
st.write(f"Displaying orders with status {status_filter}")

# Display orders succinctly
for order in orders:
    if order.status == status_filter or status_filter == 'all':
        st.write(f"Order ID: {order.id}, Status: {order.status}")