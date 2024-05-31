from front_objects.navigation import make_sidebar
import streamlit as st
import requests
make_sidebar()
import streamlit as st

st.title("ChatBot 💬")
st.write("Feel free to ask me anything! I'm here to help.")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if question := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("User"):
        st.markdown(question)
    # Add user message to chat history
    with st.chat_message("Assistant"):
        respone = requests.get(f'http://chatbot:8009/ask/{question}',json=question).json()
        st.session_state.messages.append({"role": "Assistant", "content": respone})
    st.session_state.messages.append({"role": "user", "content": question})

    