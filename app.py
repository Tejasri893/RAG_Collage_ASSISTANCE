
import streamlit as st
from groq import Groq
import os

st.set_page_config(
    page_title="AI College Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI College Assistant")
st.caption("Ask questions and get AI-generated answers.")

# Read the API key from an environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "Groq API key not found. Set the GROQ_API_KEY "
        "environment variable and restart the app."
    )
    st.stop()

client = Groq(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to AI College Assistant. "
                "Ask me about Python, AI, DBMS, or any topic "
                "you want to learn."
            )
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly AI college "
                                "assistant. Explain concepts in "
                                "simple language for beginners. "
                                "Use examples and step-by-step "
                                "explanations when helpful. "
                                "If you do not know an answer, "
                                "be honest."
                            )
                        },
                        *st.session_state.messages
                    ],
                    max_completion_tokens=700
                )

                answer = (
                    response.choices[0].message.content
                    or "Sorry, I could not generate an answer."
                )

            except Exception as error:
                answer = (
                    "Sorry, something went wrong while "
                    "generating your answer. Check your "
                    "internet connection, API key, model "
                    "availability, and Groq usage limits."
                )
                st.error(f"Error details: {error}")

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Clear chat
if st.button("🗑️ Clear conversation"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! What would you like to learn?"
        }
    ]
    st.rerun()
