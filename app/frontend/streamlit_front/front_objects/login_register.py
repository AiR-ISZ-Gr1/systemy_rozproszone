import requests
import secrets
import streamlit as st
# from .get_variables import get_variable
from string import punctuation
from .utils import Links

API_BASE_URL = Links.BACKEND_BASE_URL

def register_user(username, password):
    response = requests.post(f"{API_BASE_URL}/register", json={"username": username, "password": password})
    return response.json()

def login_user(username, password):
    response = requests.post(f"{API_BASE_URL}/login", json={"username": username, "password": password})
    return response.json()


def login_register_front():
    user_choice = st.radio("Choose an option:", ('Log In', 'Register'))

    if user_choice == 'Log In':
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Log in"):
            # response = login_user(username, password)
            if username == "aaa" and password == "aaa":
                response = {"message": "Logged in successfully."}

            if response.get('message') == 'Logged in successfully.':
                st.success("Logged in successfully!")

                session_token = secrets.token_urlsafe()
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error(response.get('message', 'Error logging in.'))

    elif user_choice == 'Register':
        st.write("Register a new account, the password have to be logner than 8 characters and has one on more specific charakter")
        new_username = st.text_input("Choose a username", key="register_username")
        new_password = st.text_input("Choose a password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")
        
        
        if st.button("Register"):
            if len(new_password) < 8 or not any(char in new_password for char in list(punctuation)):
                st.error("Password must be at least 8 characters long and and has one on more specific charakter like '#' or '@' or '$'. Please try again.")
            else:
                if new_password != confirm_password:
                    st.error("Passwords do not match. Please try again.")
                else:
                    
                    response = register_user(new_username, new_password)
                    if response.get('message') == 'User registered successfully.':
                        st.success("Registered successfully! Please log in.")
                    else:
                        st.error(response.get('message', 'Error registering.'))
