import requests
import streamlit as st
from .utils import Links
import random

class RecomendSystem:
    def __init__(self) -> None:
        self.produkty = []
        
        
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

    def wyswietl_kafelki_produktow(self):
        if len(self.produkty) == 0:
            self.produkty = self.generuj_produkty(3)
                 
        indeks_produktu = 0
        while indeks_produktu < len(self.produkty):
            col1, col2, col3, col4 = st.columns(4)
            for col in [col1, col2, col3, col4]:
                with col:
                    if indeks_produktu < len(self.produkty):
                        produkt = self.produkty[indeks_produktu]
                        if st.button(f' {produkt["nazwa"]} '):
                            st.session_state.selected_product = produkt
                            st.switch_page(Links.PRODUCT_DETAILSC)
                        # st.image(produkt["zdjecie"], width=60)
                        st.write(f"**{produkt['nazwa']}**")
                        st.write(f"Cena: {produkt['cena']}")
                        indeks_produktu += 1
                        
    def run(self):
        self.generuj_produkty(3)
        self.wyswietl_kafelki_produktow()
        
        if st.button("Refresh"):
            self.produkty.clear()
