from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
import re 

make_sidebar()

st.write(
    """
## 🛒 DANE DO WYSYŁKI

Proszę o uzupełnienie poniższych danych, abyśmy mogli dostarczyć zamówienie pod wskazany adres.
"""
)

# Funkcja do walidacji emaila
def sprawdz_email(email):
    wzor = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(wzor, email)


def wyswietl_zakupy(df):
    st.write("Twoje zakupy:")
    st.write(df)
    df['Łączna cena'] = df['Łączna cena'].str.replace('$', '').astype(float)
    suma = df['Łączna cena'].sum()
    
    st.write(f"**Łączna kwota zamówienia:** {suma} $")


# Formularz danych użytkownika
with st.form("formularz_danych"):
    st.header("Twoje dane do wysyłki:")
    imie = st.text_input("Imię:")
    nazwisko = st.text_input("Nazwisko:")
    adres = st.text_input("Adres:")
    miasto = st.text_input("Miasto:")
    kod_pocztowy = st.text_input("Kod pocztowy:")
    email = st.text_input("Email:")
    
    metoda_platnosci = st.selectbox("Wybierz metodę płatności:", ["Karta kredytowa", "Przelew bankowy", "PayPal"])
    
    submitted = st.form_submit_button("Wyślij zamówienie")
    
if submitted:
    if not all([imie, nazwisko, adres, miasto, kod_pocztowy, email]):
        st.warning("Proszę wypełnić wszystkie pola w formularzu poprawnie")
    else:
        
        st.success("Dziękujemy za złożenie zamówienia!")
        st.subheader("Podsumowanie zamówienia:")
        st.write(f"Imię: {imie}")
        st.write(f"Nazwisko: {nazwisko}")
        st.write(f"Adres: {adres}")
        st.write(f"Miasto: {miasto}")
        st.write(f"Kod pocztowy: {kod_pocztowy}")
        st.write(f"Email: {email}")
        st.write(f"Wybrana metoda płatności: {metoda_platnosci}")
        #TODO wyślij numer zamówienia na backend
        wyswietl_zakupy(st.session_state['temp_order'])
        del st.session_state["temp_order"]