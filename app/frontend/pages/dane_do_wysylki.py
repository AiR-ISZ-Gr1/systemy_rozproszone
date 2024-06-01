import streamlit as st
import pandas as pd
import re
import requests
from front_objects.navigation import make_sidebar
from pydantic import BaseModel

make_sidebar()

st.write(
    """
## 🛒 SHIPPING DETAILS

Please fill in the details below so we can deliver your order to the specified address.
"""
)

# Function to validate email
class CartItem(BaseModel):
    product_id: str
    quantity: int

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# User data form
with st.form("shipping_form"):
    st.header("Your Shipping Details:")
    first_name = st.text_input("First Name:")
    last_name = st.text_input("Last Name:")
    address = st.text_input("Address:")
    city = st.text_input("City:")
    postal_code = st.text_input("Postal Code:")
    email = st.text_input("Email:")

    payment_method = st.selectbox("Choose payment method:", [
                                  "Credit Card", "Bank Transfer", "PayPal"])

    submitted = st.form_submit_button("Submit Order")

if submitted:
    if not all([first_name, last_name, address, city, postal_code, email]) or not validate_email(email):
        st.warning("Please fill in all fields in the form correctly.")
    else:
        order_data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "postal_code": postal_code,
            "email": email,
            "payment_method": payment_method,
            "user_id": st.session_state.user_id,
            "order_summary": []
        }

        response = requests.post(
            "http://send_order:8006/submit_order/", json=order_data)

        if response.status_code == 200:
            st.success("Thank you for your order!")
            st.subheader("Order Summary:")
            st.write(f"First Name: {first_name}")
            st.write(f"Last Name: {last_name}")
            st.write(f"Address: {address}")
            st.write(f"City: {city}")
            st.write(f"Postal Code: {postal_code}")
            st.write(f"Email: {email}")
            st.write(f"Chosen Payment Method: {payment_method}")
        else:
            st.error("There was an error placing your order. Please try again.")
