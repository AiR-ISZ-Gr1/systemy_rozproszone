import streamlit as st
from time import sleep

from front_objects.navigation import make_sidebar
from front_objects.login_register import login_register_front
from front_objects.get_variables import get_variable

make_sidebar()

st.title("Welcome to Student Sandbox")

st.write("created by `Bartosz Bartoszewski', 'Adam Filapek', 'Łukasz Faruga', 'Kacper Jarzyna'")
st.session_state.logged_in = False

login_register_front()

if st.session_state.logged_in == True:
    sleep(0.2)
    st.switch_page(get_variable("MAIN_USER_PAGE"))