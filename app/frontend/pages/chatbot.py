from front_objects.navigation import make_sidebar
import streamlit as st
import requests
make_sidebar()
import streamlit as st
import json
import logging
import time

st.title("ChatBot 💬")
st.write("Feel free to ask me anything! I'm here to help.")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

def get_stream(question):
    s = requests.Session()
    with s.get(f'http://chatbot:8009/ask/{question}', timeout=5, stream=True) as resp:
        for chunk in resp:
            yield chunk.decode()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if question := st.chat_input(""):

    with st.chat_message("User"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("Assistant"):
        response =st.write_stream(get_stream(question))
        st.session_state.messages.append({"role": "Assistant", "content": response})


    