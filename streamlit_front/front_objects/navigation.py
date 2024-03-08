import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

from .get_variables import get_variable

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("Systemy rozproszone")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.write("Welcome ", st.session_state.username)

            st.page_link(f"pages/{get_variable('MAIN_USER_PAGE')}", label="Main user page", icon="🔒")
            st.page_link(f"pages/{get_variable('PAGE_2')}", label="More Secret Stuff", icon="🕵️")
            st.page_link(f"pages/{get_variable('CHATBOT_PAGE')}", label="Chatbot", icon="🕵️")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page(get_variable('MAIN_PROGRAM'))


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page(get_variable('MAIN_PROGRAM'))
    