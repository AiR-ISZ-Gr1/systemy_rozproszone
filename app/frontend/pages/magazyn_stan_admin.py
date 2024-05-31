import streamlit as st
import requests
from front_objects.navigation_admin import make_sidebar
from front_objects.product import Product

make_sidebar()
api_url = "http://magazyn_stan:8005"
a_url = "http://api:8000"

# returns products with quantity up to threshold
def get_low_stock_products(threshold: int = 5):
    response = requests.get(f"{api_url}/products/low_stock/{threshold}")
    return [Product(**product) for product in response.json()]

# restock product given their id and additional stock
def restock_product(product_id: str, additional_stock: int = 5):
    response = requests.put(f"{api_url}/products/restock/{product_id}/{additional_stock}") #, json={'product_id': product_id, 'additional_stock': additional_stock})
    return response
    # response = requests.get(f"{a_url}/products/{product_id}")
    # product_to_restock = Product(**response.json())
    # product_to_restock.quantity += additional_stock
    # response = requests.put(f"{a_url}/products/{product_id}", json=product_to_restock.dict())
    # return product_to_restock


st.title("Product Management")


low_stock_products = get_low_stock_products()
st.write(low_stock_products)

if low_stock_products:
    st.header("Products with Low Stock")
    for product in low_stock_products:
        st.subheader(f"Product ID: {product.id} - {product.name}")
        st.write(f"Price: {product.buy_price}")
        st.write(f"Current Stock: {product.quantity}")
        additional_stock = st.number_input(f"Order additional stock for {product.name}", min_value=1, max_value=100, key=product.id)
        if st.button(f"Order for {product.name}", key=f"order_{product.id}"):
            updated_product = restock_product(product.id, additional_stock)
            st.write(updated_product)
            st.success(f"Ordered additional {additional_stock} units for {product.name}. New stock: ")
else:
    st.write("No products with low stock.")
