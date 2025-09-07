import streamlit as st
from demo_chatbott import RealEstateBot


if "bot" not in st.session_state:
    st.session_state.bot = RealEstateBot()
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.title("🏠 Real Estate Chatbot")


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
