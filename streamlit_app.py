import streamlit as st
from demo_chatbott import RealEstateBot

st.set_page_config(page_title="🏠 Real Estate Chatbot", page_icon="🏡")

if "bot" not in st.session_state:
    st.session_state.bot = RealEstateBot()


if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "assistant",
         "content": "👋 Hello! I'm your Real Estate Assistant. Tell me your budget, location, and property type, and I'll find some options for you."}
    ]

st.title("🏠 Real Estate Chatbot")

if st.button("Clear"):
    st.session_state.conversation = [
        {"role": "assistant",
         "content": "👋 Hello! I'm your Real Estate Assistant. Tell me your budget, location, and property type, and I'll find some options for you."}
    ]
    st.session_state.bot = RealEstateBot()


user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state.conversation.append({"role": "user", "content": user_input})

    response, leads = st.session_state.bot.chat(user_input)

    st.session_state.conversation.append({"role": "assistant", "content": response})

for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])


