import streamlit as st
import pandas as pd
import re
import requests
from front_objects.navigation import make_sidebar

make_sidebar()

st.write(
    """
## 🛒 DANE DO WYSYŁKI

Proszę o uzupełnienie poniższych danych, abyśmy mogli dostarczyć zamówienie pod wskazany adres.
"""
)

# Function to validate email


def sprawdz_email(email):
    wzor = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(wzor, email)


# User data form
with st.form("formularz_danych"):
    st.header("Twoje dane do wysyłki:")
    imie = st.text_input("Imię:")
    nazwisko = st.text_input("Nazwisko:")
    adres = st.text_input("Adres:")
    miasto = st.text_input("Miasto:")
    kod_pocztowy = st.text_input("Kod pocztowy:")
    email = st.text_input("Email:")

    metoda_platnosci = st.selectbox("Wybierz metodę płatności:", [
                                    "Karta kredytowa", "Przelew bankowy", "PayPal"])

    submitted = st.form_submit_button("Wyślij zamówienie")

if submitted:
    if not all([imie, nazwisko, adres, miasto, kod_pocztowy, email]) or not sprawdz_email(email):
        st.warning("Proszę wypełnić wszystkie pola w formularzu poprawnie")
    else:
        order_data = {
            "first_name": imie,
            "last_name": nazwisko,
            "address": adres,
            "city": miasto,
            "postal_code": kod_pocztowy,
            "email": email,
            "payment_method": metoda_platnosci,
            "user_id": st.state.user_id,
        }

        response = requests.post(
            "http://send_order:8006/submit_order/", json=order_data)

        if response.status_code == 200:
            st.success("Dziękujemy za złożenie zamówienia!")
            st.subheader("Podsumowanie zamówienia:")
            st.write(f"Imię: {imie}")
            st.write(f"Nazwisko: {nazwisko}")
            st.write(f"Adres: {adres}")
            st.write(f"Miasto: {miasto}")
            st.write(f"Kod pocztowy: {kod_pocztowy}")
            st.write(f"Email: {email}")
            st.write(f"Wybrana metoda płatności: {metoda_platnosci}")
        else:
            st.error(
                "Wystąpił błąd podczas składania zamówienia. Proszę spróbować ponownie.")
