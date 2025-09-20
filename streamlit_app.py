import streamlit as st
from demo_chatbott import RealEstateBot
import uuid, json
from pathlib import Path

LIMIT = 100
FILE = Path("usage.json")

def load_usage():
    return json.loads(FILE.read_text()) if FILE.exists() else {}

def save_usage(data):
    FILE.write_text(json.dumps(data))

if "user_id" not in st.session_state:
    uid_from_url = st.query_params.get("uid", [None])[0]
    if uid_from_url:
        st.session_state.user_id = uid_from_url
    else:
        st.session_state.user_id = str(uuid.uuid4())
        st.experimental_set_query_params(uid=st.session_state.user_id)

usage = load_usage()
tokens = usage.get(st.session_state.user_id, 0)

if tokens > LIMIT:
    st.error("Demo limit reached.")
    st.stop()

WELCOME = "👋 Hi! I’m PrimeProp AI, here to help you discover the perfect home or investment."

st.set_page_config(page_title="🏠 Real Estate Chatbot", page_icon="🏡")
st.title("🏠 Real Estate Chatbot")


if "bot" not in st.session_state:
    st.session_state.bot = RealEstateBot()
    st.session_state.bot.messages.append({"role": "assistant", "content": WELCOME})

if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "assistant", "content": WELCOME}]

if st.button("Clear"):
    st.session_state.bot = RealEstateBot()
    st.session_state.bot.messages.append({"role": "assistant", "content": WELCOME})
    st.session_state.conversation = [{"role": "assistant", "content": WELCOME}]


for msg in st.session_state.conversation:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Type your message here...")
if user_input:

    st.session_state.conversation.append({"role": "user", "content": user_input})


    response, _ = st.session_state.bot.chat(user_input)
    st.session_state.conversation.append({"role": "assistant", "content": response})


    usage[st.session_state.user_id] = tokens + len(response)
    save_usage(usage)

