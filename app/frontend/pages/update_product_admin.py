import streamlit as st
import requests

from front_objects.navigation_admin import make_sidebar
make_sidebar()

api_url = "http://update_product:8003"

st.title("Shop Management System")

# Fetch product list
response = requests.get(f"{api_url}/products")
products = response.json()

# Select a product to edit
product_ids = [product["id"] for product in products]
selected_product_id = st.selectbox("Select a product to edit", product_ids)

if selected_product_id:
    response = requests.get(f"{api_url}/product/{selected_product_id}")
    selected_product = response.json()

    st.write("### Edit Product")
    name = st.text_input("Name", selected_product["name"])
    description = st.text_area("Description", selected_product["description"])
    price = st.number_input("Price", value=selected_product["price"])
    image_url = st.text_input("Image URL", selected_product["image_url"])

    if st.button("Update Product"):
        updated_product = {
            "id": selected_product_id,
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url
        }
        response = requests.put(f"{api_url}/product/{selected_product_id}", json=updated_product)
        if response.status_code == 200:
            st.success("Product updated successfully")
        else:
            st.error("Failed to update product")
