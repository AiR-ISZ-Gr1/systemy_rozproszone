from front_objects.navigation import make_sidebar
import streamlit as st
from front_objects.utils import Links
import requests
import random

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

        produkty = self.generuj_produkty(10)
        self.wyswietl_kafelki_produktow(produkty)

    @staticmethod
    @st.cache_data
    def ask_products(number):
        url = "http://127.0.0.1:8000/produkty/"
        params = {'N': number}
        produkty = requests.get(url, params=params)
        print(produkty.json())
        return produkty.json()

    @staticmethod
    @st.cache_data
    def generuj_produkty(N):
        produkty = []
        for i in range(1, N+1):
            cena = "${:.2f}".format(random.uniform(5, 50))  # Losowa cena w przedziale od $5.00 do $50.00
            nazwa = f"Produkt {i}"
            opis = f"To jest opis {nazwa}"
            produkt = {"nazwa": nazwa, "zdjecie": "test.jpg", "cena": cena, "opis": opis}
            produkty.append(produkt)
        return produkty

    @staticmethod
    @st.cache_data
    def filtrowanie_produktow(produkty, fraza):
        return [produkt for produkt in produkty if produkt['nazwa'].lower().startswith(fraza.lower())]

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
                        if st.button(produkt["nazwa"]):
                            st.session_state.selected_product = produkt
                            st.switch_page(Links.PRODUCT_DETAILSC)
                        st.image(produkt["zdjecie"], width=100, use_column_width=False, clamp=False)
                        st.write(f"**{produkt['nazwa']}**")
                        st.write(f"Cena: {produkt['cena']}")
                        indeks_produktu += 1

# class ProductDetailsApp:
#     @staticmethod
#     def run():
#         st.text(st.session_state.selected_product["nazwa"])
#         st.image(st.session_state.selected_product["zdjecie"], use_column_width=True, clamp=True)
#         st.write(f"**Nazwa:** {st.session_state.selected_product['nazwa']}")
#         st.write(f"**Cena:** {st.session_state.selected_product['cena']}")
#         st.subheader("Opcje produktu:")
#         if st.button("Dodaj do koszyka"):
#             st.success("Produkt dodany do koszyka!")
#         if st.button("Przeglądaj opinie"):
#             st.info("Opinie o produkcie")
#             st.write("1. Bardzo dobry produkt!")
#             st.write("2. Trochę za drogi jak na tę jakość.")
#         st.subheader("Dodaj własną opinię:")
#         opinia = st.text_area("Wpisz swoją opinię")
#         if st.button("Dodaj opinię"):
#             if opinia:
#                 st.success("Twoja opinia została dodana pomyślnie!")
#             else:
#                 st.warning("Wpisz treść opinii przed dodaniem.")
#         if st.button("Powrót do wszystkich produktów"):
#             del st.session_state.selected_product

app = SecretCompanyApp()
app.run()