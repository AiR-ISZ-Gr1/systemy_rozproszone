import streamlit as st
import requests
from pydantic import BaseModel, Field
import nanoid

from front_objects.navigation_admin import make_sidebar
make_sidebar()
from PIL import Image
from io import BytesIO
from front_objects.product import Product

def show_photo(product_photo_id: str):
    photo_url_dowland = "http://api:8000/files/download/"
    response = requests.get(f"{photo_url_dowland}{product_photo_id}", stream=True)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        return None
    
def compress_image(image: Image.Image, output_size=(640, 640), quality=20) -> BytesIO:
    image.thumbnail(output_size)
    output = BytesIO()
    image.save(output, format='png', quality=quality)
    output.seek(0)
    return output

# api_url = "http://update_product:8003"
api_url = "http://api:8000"
photo_url = "http://api:8000/files/upload"

st.title("Shop Management System")

# Fetch product list
response = requests.get(f"{api_url}/products")
products = response.json()

# Select a product to edit
product_ids = [product["id"] for product in products]
selected_product_id = st.selectbox("Select a product to edit", product_ids)

if selected_product_id:
    response = requests.get(f"{api_url}/products/{selected_product_id}")
    # st.write("resp:", response.json())
    selected_product = response.json()
    
    
    st.write("### Edit Product")
    
    # st.write("API Response:", selected_product)
    name = st.text_input("Name", selected_product["name"])
    description = st.text_area("Description", selected_product["description"])
    sell_price = st.number_input("Sell price", value=selected_product["sell_price"])
    quantity = st.number_input("Quantity", value=selected_product["quantity"])
    buy_price = st.number_input("Buy price", value=selected_product["buy_price"])
    tags = st.multiselect(
    "Categories",
    ["Flower", "Tree", "Object", "Other", "Manure"],
    ["Flower"])
    image_show = show_photo(selected_product["image_id"])
    if image_show:
        st.image(image_show)
    image = st.file_uploader("Image", type=['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'])
    
    if st.button("Update Product"):
        updated_product = Product(
            name=name,
            description=description,
            sell_price=sell_price,
            quantity=quantity,
            buy_price=buy_price,
            tags=tags
        )

        if image is None:
            image_id = selected_product["image_id"]
        else:
            updated_product.add_product_image(image)
            # # Create a file-like object for the compressed image
            # files = {'file': image.getvalue()}
            # response1 = requests.post(photo_url, files=files)
            # image_id = response1.json()['file_id']
            
        response = requests.put(f"{api_url}/products/{selected_product_id}", json=updated_product.dict())
        
        if response.status_code == 200:
            st.success("Product updated successfully")
        else:
            st.error("Failed to update product")
