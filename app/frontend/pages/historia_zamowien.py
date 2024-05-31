import streamlit as st
import requests
from front_objects.navigation import make_sidebar
from front_objects.utils import Links

make_sidebar()


def get_order_history(username):
    try:
        response = requests.get(f"http://history_order:8007/orders/{username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        pass
        # st.error(f"An error occurred: {err}")


def display_order_details(order):
    st.markdown(f"### Szczegóły zamówienia o ID #{order['order_id']}")

    st.markdown(f"**Status Zamówienia:** {order['status']}")

    st.markdown("#### Produkty:")
    for product in order['products']:
        st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <strong>Produkt:</strong> {product['name']}<br>
            <strong>Cena:</strong> ${product['price']}<br>
        </div>
        """, unsafe_allow_html=True)

        if order['status'] == "Dostarczone" and not product['review']:
            with st.expander(f"Dodaj opinię o produkcie {product['name']}"):
                review_text = st.text_area(
                    "Twoja opinia", key=f"review_text_{order['order_id']}_{product['name']}")
                if st.button("Wyślij opinię", key=f"submit_button_{order['order_id']}_{product['name']}"):
                    send_review(
                        username, order['order_id'], product['name'], review_text)


def send_review(username, order_id, product, review):
    review_data = {
        "username": username,
        "order_id": order_id,
        "product": product,
        "review": review
    }
    try:
        response = requests.post(
            "http://history_orders:8007/review", json=review_data)
        response.raise_for_status()
        st.success(f"Opinia dla produktu {product} została wysłana pomyślnie!")
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


st.title("Historia twoich zamówień")

username = st.session_state.get("username", None)

if username:
    orders = get_order_history(st.session_state.user_id)
    if orders:
        for order in orders:
            if st.button(f"Zamówienie #{order['order_id']}"):
                st.session_state[f"expanded_order_{order['order_id']}"] = not st.session_state.get(
                    f"expanded_order_{order['order_id']}", False)

        for order in orders:
            if st.session_state.get(f"expanded_order_{order['order_id']}", False):
                display_order_details(order)
    else:
        st.write("No orders found!")
