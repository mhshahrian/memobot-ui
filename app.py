import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="Memory Chatbot")
st.title("✨ Memory Chatbot")

user_id = "user_1"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    message = st.text_input("You:", key="input")
    submitted = st.form_submit_button("Send")

# Handle submission
if submitted and message:
    # Add user message to history
    st.session_state.chat_history.append(("You", message))

    try:
        # Call the chatbot API
        response = requests.post(
            "https://memory-chat-backend-718486642397.us-central1.run.app/chat",
            json={"user_id": user_id, "message": message}
        )
        data = response.json()
        reply = data.get("reply", "⚠️ No reply received.")
        memory_used = data.get("memory_used", False)
        related_memories = data.get("related_memories", [])
    except Exception as e:
        reply = f"⚠️ Error: {e}"
        memory_used = False
        related_memories = []

    # Add bot response to history
    st.session_state.chat_history.append((
        "Bot",
        {
            "reply": reply,
            "memory_used": memory_used,
            "related_memories": related_memories
        }
    ))

# Display chat history (newest messages first)
for speaker, content in reversed(st.session_state.chat_history):
    if speaker == "You":
        st.markdown(f"**🧑 You:** {content}")
    else:
        st.markdown(f"**🤖 Bot:** {content['reply']}")
        st.markdown(f"🧠 **Memory Used:** {'Yes' if content['memory_used'] else 'No'}")
