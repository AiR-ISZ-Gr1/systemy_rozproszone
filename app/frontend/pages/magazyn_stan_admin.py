import streamlit as st
import requests
from front_objects.navigation_admin import make_sidebar
from front_objects.product import Product

make_sidebar()
api_url = "http://api:8000"

def get_low_stock_products():
    response = requests.get(f"{api_url}/products/low_stock/")
    return response.json()

def order_product(product_id, additional_stock):
    response = requests.put(f"{api_url}/products/{product_id}", json={"additional_stock": additional_stock})
    return response.json()

st.title("Product Management")

low_stock_products = get_low_stock_products()

if low_stock_products:
    st.header("Products with Low Stock")
    for product in low_stock_products:
        st.subheader(f"Product ID: {product['id']} - {product['name']}")
        st.write(f"Price: {product['price']}")
        st.write(f"Current Stock: {product['stock']}")
        additional_stock = st.number_input(f"Order additional stock for {product['name']}", min_value=1, max_value=100, key=product['id'])
        if st.button(f"Order for {product['name']}", key=f"order_{product['id']}"):
            updated_product = order_product(product['id'], additional_stock)
            st.success(f"Ordered additional {additional_stock} units for {product['name']}. New stock: {updated_product['stock']}")
else:
    st.write("No products with low stock.")
