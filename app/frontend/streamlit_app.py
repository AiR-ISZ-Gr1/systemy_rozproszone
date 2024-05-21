import streamlit as st
from time import sleep

from front_objects.navigation import make_sidebar
from front_objects.login_register import login_register_front
from front_objects.utils import Links

# make_sidebar()

st.title("**Welcome our plant shop!**")

st.write("created by **Bartosz Bartoszewski**, **Adam Filapek**, **Łukasz Faruga**, **Kacper Jarzyna**")
st.session_state.logged_in = False

login_register_front()

if st.session_state.logged_in == True:
    if st.session_state.is_admin:
        st.write("You are logged in as an admin.")
    else:
        sleep(0.2)
        print()
        st.switch_page(Links.MAIN_USER_PAGE)