# import streamlit as st
# from predict import get_response
#
# st.set_page_config(page_title="ML chatbot", layout="wide")
#
# st.title("ML chatbot")
# st.write("Chatbot with intent..")
#
# user_input = st.text_input("Enter your query")
# if "chat_history" not in st.session_state:
#     st.session_state["chat_history"] = []
#
# if st.button("Send") and user_input.strip() != "":
#     st.session_state["chat_history"].append(("You", user_input))
#     response = get_response(user_input)
#     st.session_state["chat_history"].append(("Chatbot", response))
#
# for sender, message in st.session_state["chat_history"]:
#     if sender=="You":
#         st.markdown(f"**You:** {message}")
#     else:
#         st.markdown(message)
#



import streamlit as st
from predict import get_response

st.set_page_config(page_title="ML Chatbot", layout="wide")

st.title("🤖 ML Intent Chatbot")
st.write("Chatbot powered by Machine Learning")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.write(message)

# Chat input box (modern Streamlit style)
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.chat_history.append(("You", user_input))

    # Get ML-based response
    response = get_response(user_input)

    # Add bot response
    st.session_state.chat_history.append(("Bot", response))

    # Rerun to display updated chat
    st.rerun()

# Optional: Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()