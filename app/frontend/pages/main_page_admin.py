import streamlit as st
import requests
from datetime import datetime
from front_objects.navigation_admin import make_sidebar
make_sidebar()

st.title('Dodaj nowy produkt')

nazwa = st.text_input('Nazwa produktu')
opis = st.text_area('Opis produktu')
cena_sprzedazy = st.number_input('Cena sprzedaży produktu', min_value=0.0, format="%.2f")
ilosc_dostepnych_sztuk = st.number_input('Ilość dostępnych sztuk', min_value=0)
cena_zakupu = st.number_input('Cena zakupu produktu', min_value=0.0, format="%.2f")
data_wprowadzenia = st.date_input('Data wprowadzenia produktu', value=datetime.today())
zdjecie = st.file_uploader('Zdjęcie produktu', type=['jpg', 'jpeg', 'png'])

if st.button('Dodaj produkt'):
    if nazwa and opis and cena_sprzedazy and ilosc_dostepnych_sztuk and cena_zakupu and data_wprowadzenia and zdjecie:
        # Przygotowanie danych do wysłania
        files = {'zdjecie': zdjecie.getvalue()}
        data = {
            'nazwa': nazwa,
            'opis': opis,
            'cena_sprzedazy': cena_sprzedazy,
            'ilosc_dostepnych_sztuk': ilosc_dostepnych_sztuk,
            'cena_zakupu': cena_zakupu,
            'data_wprowadzenia': data_wprowadzenia.strftime('%Y-%m-%d')
        }

        # Wysłanie danych do FastAPI
        api_callback='http://collect_products:8002'
        response = requests.post(f'{api_callback}/products/', data=data, files=files)

        if response.status_code == 200:
            st.success('Produkt został dodany pomyślnie!')
        else:
            st.error('Wystąpił błąd podczas dodawania produktu.')
    else:
        st.warning('Proszę wypełnić wszystkie pola.')

