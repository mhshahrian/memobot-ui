import streamlit as st
import requests

st.set_page_config(page_title="Memory Chatbot")
st.title("✨ Memory Chatbot")

user_id = "test_user"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

message = st.text_input("You:", key="input")

if message:
    st.session_state.chat_history.append(("You", message))
    
    try:
        response = requests.post(
            "https://memory-chat-backend-718486642397.us-central1.run.app/chat",
            json={"user_id": user_id, "message": message}
        )
        reply = response.json().get("response", "⚠️ No reply received.")
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    
    st.session_state.chat_history.append(("Bot", reply))

# Display chat history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")
