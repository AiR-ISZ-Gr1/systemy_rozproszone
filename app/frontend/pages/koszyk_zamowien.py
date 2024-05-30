from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests

make_sidebar()

base_url = "http://api:8000"


st.write(
    """
# 🛒 KOSZYK ZAMÓWIEŃ

Tutaj znajdziesz wszystkie produkty, które dodałeś do koszyka.
"""
)

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()

for i in get_items_in_cart:
    get_item_name = str(i["product_id"])
    choosen_quantity = i["quantity"]
    
    get_item_details = requests.get(f"{base_url}/products/{get_item_name}").json()
    get_item_name = get_item_details["name"]
    get_item_price = get_item_details["sell_price"]
    get_accual_quantity = get_item_details["quantity"]
    
    st.subheader(f"**:** {get_item_name}")
    st.write(f"**Cena za sztukę:** {get_item_price} $")
    st.write(f"**Wybrana ilość:** {choosen_quantity}")
    st.write(f"**Dostępna ilość:** {get_accual_quantity}")

# # Sprawdź czy użytkownik jest zalogowany i czy istnieje lista zakupów w sesji
# if 'username' in st.session_state and 'lista_zakupow' in st.session_state:
#     nazwa_uzytkownika = st.session_state.username
#     lista_zakupow = st.session_state.lista_zakupow
    
#     # Sprawdź czy użytkownik ma produkty w koszyku
#     if nazwa_uzytkownika in lista_zakupow:
#         koszyk = lista_zakupow[nazwa_uzytkownika]["produkty"]
        
#         df = pd.DataFrame(koszyk)
#         df = df.groupby(['nazwa', 'cena'])['ilość'].sum().reset_index()
#         # Dodaj możliwość zmiany ilości produktów
#         for index, row in df.iterrows():
#             new_quantity = st.number_input(f"Ilość {row['nazwa']}", min_value=0, value=row['ilość'])
#             if new_quantity != row['ilość']:
#                 df.at[index, 'ilość'] = new_quantity
        
#         df['cena2'] = df['cena'].replace({'\$': ''}, regex=True).astype(float)
#         df_sum = df.groupby('nazwa').agg({'cena2': 'first', 'ilość': 'sum'}).reset_index()
#         df['Łączna cena'] = '$' + (df['cena2'] * df['ilość']).astype(str)
#         del df['cena2']
        
#         st.write(df)
        
#         # Oblicz łączną kwotę zamówienia
#         df['cena_2'] = df['Łączna cena'].str.replace('$', '').astype(float)
#         suma = df['cena_2'].sum()
#         del df['cena_2']
#         st.write(f"**Łączna kwota zamówienia:** {suma} $")
        
#         if st.button("Podsumuj zamówienie"):
#             st.session_state["temp_order"] = df
#             st.switch_page(Links.SEND_PAGE)
#             # Tutaj możesz dodać kod odpowiedzialny za finalizację zamówienia, np. wysłanie potwierdzenia
#             # TODO: dodać funkcję przekazywania argumentów na backend w celu zapisania zamówienia w bazie danych
#             # TODO: dodać funkcję, która zwraca kod potwierdzenia zamówienia
#     else:
#         st.write("Brak produktów w koszyku.")
# else:
    
#     st.write("Użytkownik nie jest zalogowany lub nie dodał jeszcze żadnych produktów do koszyka.")
