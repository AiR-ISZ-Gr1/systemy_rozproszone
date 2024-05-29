import streamlit as st
import requests
from pydantic import BaseModel, Field
import nanoid

from front_objects.navigation_admin import make_sidebar
make_sidebar()

api_url = "http://update_product:8003"

st.title("Shop Management System")

# Fetch product list
response = requests.get(f"{api_url}/products")
products = response.json()

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sale_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str
    picture_path: str

# Select a product to edit
product_ids = [product["id"] for product in products]
selected_product_id = st.selectbox("Select a product to edit", product_ids)

if selected_product_id:
    st.write("ID:", selected_product_id)
    response = requests.get(f"{api_url}/product/{selected_product_id}")
    st.write("resp:", response)
    selected_product = response.json()
    print(selected_product)

    st.write("### Edit Product")
    
    st.write("API Response:", selected_product)
    name = st.text_input("Name", selected_product["name"])
    description = st.text_area("Description", selected_product["description"])
    sale_price = st.number_input("Sale price", value=selected_product["sale_price"])
    quantity = st.number_input("Quantity", value=selected_product["quantity"])
    buy_price = st.number_input("Buy price", value=selected_product["buy_price"])
    image_url = st.text_input("Image URL", selected_product["picture_path"])

    if st.button("Update Product"):
        updated_product = Product(
            name=name,
            description=description,
            sale_price=sale_price,
            quantity=quantity,
            buy_price=buy_price,
            date='date',
            picture_path=image_url
        )

        response = requests.put(f"{api_url}/product/{selected_product_id}", json=updated_product)
        if response.status_code == 200:
            st.success("Product updated successfully")
        else:
            st.error("Failed to update product")
