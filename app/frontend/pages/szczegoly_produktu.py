import streamlit as st
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
import requests
from front_objects.classes.product import Product


base_url = "http://api:8000"


def get_product(product_id: str):
    response = requests.get(f"{base_url}/products/{product_id}")
    return response.json()


def wyswietl_szczegoly_produktu():
    product_details = get_product(st.session_state.selected_product_id)
    
    choosen_product = Product(**product_details)
    
    st.title(choosen_product.name)
    
    picute = choosen_product.show_photo()
    if picute:
        st.image(picute)
    
    st.write(f"**Cena:** {choosen_product.sell_price}")
    st.write(f"**Opis:** {choosen_product.description}")
    st.subheader("Zakup produktu:")
    if int(choosen_product.quantity) > 0:
        ilosc = st.number_input("Wybierz ilość produktu", min_value=1, value=1, max_value=int(choosen_product.quantity))
    else:
        st.warning("Produkt niedostępny")
        
    if st.button("Dodaj do koszyka"):
        user_id = st.session_state.user_id
        check_cart = requests.get(f"{base_url}/users/{user_id}/cart")

        
        if check_cart.status_code == 404:
            create_cart = requests.post(f"{base_url}/users/{user_id}/cart", json={})
            add_product = requests.post(f"{base_url}/users/{user_id}/cart/items", json={"product_id": choosen_product.id, "quantity": ilosc})
            
        else:
            add_product = requests.post(f"{base_url}/users/{user_id}/cart/items", json={"product_id": choosen_product.id, "quantity": ilosc})
            st.write(add_product)
        
        # czy uzytkownik posiada koszyk
        # jesli nie to stworz koszyk i dodaj produkt
        # st.error("Funkcjonalność dodawania produktu do koszyka nie jest jeszcze zaimplementowana")
        
    if st.button("Przeglądaj opinie"):
        st.info("Opinie o produkcie")
        st.write("1. Bardzo dobry produkt!")
        st.write("2. Trochę za drogi jak na tę jakość.")
    
    if st.button("Powrót do wszystkich produktów"):
            del st.session_state.selected_product_id
            st.switch_page(Links.ALL_PRODUCTS)

    st.write(f"**Category:** {choosen_product.tags}")
    # st.write(choosen_product.tags)

make_sidebar()
wyswietl_szczegoly_produktu()
