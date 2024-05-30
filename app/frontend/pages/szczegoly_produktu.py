import streamlit as st
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
import requests
photo_url = "http://api:8000/files/download/"
base_url = "http://api:8000"


def get_product(product_id: str):
    response = requests.get(f"{base_url}/products/{product_id}")
    return response.json()
    
if 'lista_zakupow' not in st.session_state:
    st.session_state.lista_zakupow = {}

def dodaj_do_koszyka(ilosc=1):
    nazwa_uzytkownika = st.session_state.username
    produkt = {
        "nazwa": st.session_state.selected_product["nazwa"],
        "cena": st.session_state.selected_product["cena"],
        "ilość": ilosc
    }
    
    
    if nazwa_uzytkownika in st.session_state.lista_zakupow:
        st.session_state.lista_zakupow[nazwa_uzytkownika]["produkty"].append(produkt)
    else:
        st.session_state.lista_zakupow[nazwa_uzytkownika] = {"produkty": [produkt]}
    
    st.success("Produkt dodany do koszyka!")

def wyswietl_szczegoly_produktu():
    product_details = get_product(st.session_state.selected_product_id)
    st.title(st.session_state.selected_product_id)
    
    st.write(product_details)
    # st.image(st.session_state.selected_product["zdjecie"], use_column_width=True, clamp=True)
    # st.write(f"**Nazwa:** {st.session_state.selected_product['nazwa']}")
    # st.write(f"**Cena:** {st.session_state.selected_product['cena']}")
    # st.write(f"**Opis:** {st.session_state.selected_product['opis']}")
    st.subheader("Opcje produktu:")
    ilosc = st.number_input("Ilość", min_value=1, value=1)
    if st.button("Dodaj do koszyka"):
        
        # Tutaj możesz dodać kod obsługujący dodawanie produktu do koszyka
        dodaj_do_koszyka(ilosc)
        
    if st.button("Przeglądaj opinie"):
        # Tutaj możesz dodać kod obsługujący przeglądanie opinii o produkcie
        st.info("Opinie o produkcie")
        # Przykładowe opinie
        st.write("1. Bardzo dobry produkt!")
        st.write("2. Trochę za drogi jak na tę jakość.")
    # Dodaj własną opinię
    st.subheader("Dodaj własną opinię:")
    
    if st.button("Powrót do wszystkich produktów"):
            del st.session_state.selected_product
            st.switch_page(Links.ALL_PRODUCTS)


make_sidebar()
wyswietl_szczegoly_produktu()
