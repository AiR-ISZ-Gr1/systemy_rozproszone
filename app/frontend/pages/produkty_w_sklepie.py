import streamlit as st
import aiohttp
import asyncio
from pydantic import BaseModel, Field
from nanoid import generate
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
photo_url = "http://api:8000/files/download/"
import requests
from io import BytesIO
from PIL import Image
from typing import List
import nanoid
import datetime


class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)
    
class SecretCompanyApp:
    def __init__(self):
        make_sidebar()

    def run(self):
        st.write(
            """
        # 🛍️ Secret Company
        Feel Free, buy everything you want!
        """
        )

        produkty = asyncio.run(self.ask_products(10))
        self.wyswietl_kafelki_produktow(produkty)

    @staticmethod
    async def get_all_products():
        base_url = "http://api:8000"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/products/") as response:
                products = await response.json()
                return [Product(**product) for product in products]

    @staticmethod
    # @st.cache_data
    async def ask_products(number):
        produkty = await SecretCompanyApp.get_all_products()
        return produkty[:number]
    
    @staticmethod
    def show_photo(product_photo_id: str):
        response = requests.get(f"{photo_url}{product_photo_id}", stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None
    
    @staticmethod
    # @st.cache_data
    def filtrowanie_produktow(produkty, fraza):
        return [produkt for produkt in produkty if produkt.name.lower().startswith(fraza.lower())]

    @staticmethod
    def wyswietl_kafelki_produktow(produkty):
        fraza = st.text_input("Filtruj produkty po nazwie:")
        wyniki_filtrowania = SecretCompanyApp.filtrowanie_produktow(produkty, fraza)
        
        indeks_produktu = 0
        while indeks_produktu < len(wyniki_filtrowania):
            col1, col2, col3, col4 = st.columns(4)
            for col in [col1, col2, col3, col4]:
                with col:
                    if indeks_produktu < len(wyniki_filtrowania):
                        produkt = wyniki_filtrowania[indeks_produktu]
                        if st.button(produkt.name, key=produkt.id):
                            st.session_state.selected_product_id = produkt.id
                            st.switch_page(Links.PRODUCT_DETAILSC)
                        image = SecretCompanyApp.show_photo(produkt.image_id)
                        st.write(produkt.image_id)
                        if image:
                            st.image(image, width=100)
                        st.write(f"**{produkt.name}**")
                        st.write(f"Cena: ${produkt.sell_price:.2f}")
                        indeks_produktu += 1

app = SecretCompanyApp()
app.run()
