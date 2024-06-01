import streamlit as st
import requests
import datetime
from front_objects.navigation_admin import make_sidebar
from front_objects.order import Order
make_sidebar()

API_URL = "http://change_order_status:8004"

def fetch_orders(status='all'):
    response = requests.get(f"{API_URL}/orders", params={"status": status})
    if response.status_code == 200:
        return [Order(**order) for order in response.json()]
    else:
        return []

# def fetch_orders(status=None):
#     if status:
#         response = requests.get(f"{API_URL}/orders", params={"status": status})
#     else:
#         response = requests.get(f"{API_URL}/orders")
#     if response.status_code == 200:
#         return [Order(**order) for order in response.json()]
#     else:
#         return []

def fetch_order_by_id(order_id):
    response = requests.get(f"{API_URL}/orders/{order_id}")
    if response.status_code == 200:
        return Order(**response.json())
    else:
        return None

def update_order_status(order_id, status):
    response = requests.put(f"{API_URL}/orders/{order_id}", params={"status": status})
    return response.status_code == 200

st.title("Order Management System")

search_id = st.text_input("Enter Order ID to search")

if search_id:
    order = fetch_order_by_id(search_id)
    if order:
        st.write(f"Order ID: {order.id}")
        st.write(f"Order Date: {order.date}")
        st.write(f"Customer ID: {order.user_id}")
        st.write(f"Status: {order.status}")
        
        new_status = st.selectbox("Change Status", ["cancelled", "ready to ship", "shipped"], key=order.id)
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

status_filter = st.selectbox("Filter by Status", ["all", "new", "cancelled", "ready to ship", "shipped"])

if status_filter == "all":
    orders = fetch_orders()
else:
    orders = fetch_orders(status=status_filter)

st.write(f"Displaying {len(orders)} orders with status {status_filter}")

# Display orders succinctly
for order in orders:
    st.write(f"Order ID: {order.id}, Status: {order.status}")