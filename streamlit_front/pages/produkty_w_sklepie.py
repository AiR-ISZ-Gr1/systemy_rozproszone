from front_objects.navigation import make_sidebar
import streamlit as st

make_sidebar()

st.write(
    """
# 🛍️ Secret Company
Tut jest wszystko, ale nic dla ciebie.
"""
)

produkty = [
    {"nazwa": "Produkt 1", "zdjecie": "test.jpg", "cena": "$19.99", "opis": "To jest opis Produktu 1"},
    {"nazwa": "Produkt 2", "zdjecie": "test.jpg", "cena": "$24.99", "opis": "To jest opis Produktu 2"},
    {"nazwa": "Produkt 3", "zdjecie": "test.jpg", "cena": "$14.99", "opis": "To jest opis Produktu 3"},
    {"nazwa": "Produkt 4", "zdjecie": "test.jpg", "cena": "$29.99", "opis": "To jest opis Produktu 4"},
    {"nazwa": "Produkt 5", "zdjecie": "test.jpg", "cena": "$9.99", "opis": "To jest opis Produktu 5"},
    {"nazwa": "Produkt 6", "zdjecie": "test.jpg", "cena": "$34.99", "opis": "To jest opis Produktu 6"},
    # Dodaj więcej produktów według potrzeb
]

def filtrowanie_produktow(produkty, fraza):
    return [produkt for produkt in produkty if produkt['nazwa'].lower().startswith(fraza.lower())]

def wyswietl_kafelki_produktow():
    # Strona główna z kafelkami produktów
    st.title("Sklep internetowy")

    # Pole tekstowe do wprowadzania frazy
    fraza = st.text_input("Filtruj produkty po nazwie:")

    # Filtrowanie produktów po wprowadzonej frazie
    wyniki_filtrowania = filtrowanie_produktow(produkty, fraza)

    # Liczba kafelków na produkt w jednym rzędzie

    indeks_produktu = 0
    while indeks_produktu < len(wyniki_filtrowania):
        # Tworzenie rzędu kafelków produktów
        col1, col2, col3, col4 = st.columns(4)
        
        for col in [col1, col2, col3, col4]:
            with col:
                if indeks_produktu < len(wyniki_filtrowania):
                    produkt = wyniki_filtrowania[indeks_produktu]
                    if st.button(produkt["nazwa"]):
                        st.session_state.selected_product = produkt
                    st.image(produkt["zdjecie"], width=100, use_column_width=False, clamp=False)
                    st.write(f"**{produkt['nazwa']}**")
                    st.write(f"Cena: {produkt['cena']}")
                    indeks_produktu += 1

# Strona szczegółów produktu
def wyswietl_szczegoly_produktu():
    st.title(st.session_state.selected_product["nazwa"])
    st.image(st.session_state.selected_product["zdjecie"], use_column_width=True, clamp=True)
    st.write(f"**Nazwa:** {st.session_state.selected_product['nazwa']}")
    st.write(f"**Cena:** {st.session_state.selected_product['cena']}")
    # st.write(f"**Opis:** {st.session_state.selected_product['opis']}")
    st.subheader("Opcje produktu:")
    if st.button("Dodaj do koszyka"):
        # Tutaj możesz dodać kod obsługujący dodawanie produktu do koszyka
        st.success("Produkt dodany do koszyka!")
    if st.button("Przeglądaj opinie"):
        # Tutaj możesz dodać kod obsługujący przeglądanie opinii o produkcie
        st.info("Opinie o produkcie")
        # Przykładowe opinie
        st.write("1. Bardzo dobry produkt!")
        st.write("2. Trochę za drogi jak na tę jakość.")
    # Dodaj własną opinię
    st.subheader("Dodaj własną opinię:")
    opinia = st.text_area("Wpisz swoją opinię")
    if st.button("Dodaj opinię"):
        # Tutaj możesz dodać kod obsługujący dodawanie własnej opinii
        if opinia:
            st.success("Twoja opinia została dodana pomyślnie!")
        else:
            st.warning("Wpisz treść opinii przed dodaniem.")
    if st.button("Powrót do wszystkich produktów"):
            del st.session_state.selected_product


if "selected_product" in st.session_state:
    wyswietl_szczegoly_produktu()
else:
    wyswietl_kafelki_produktow()




