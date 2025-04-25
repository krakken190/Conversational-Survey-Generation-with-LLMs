import streamlit as st
import os
import json
import re
from openai import OpenAI
# from dotenv import load_dotenv
from datetime import datetime

import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded


# environment variables
# load_dotenv()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# response directory exists
os.makedirs("response", exist_ok=True)

# Profanity word list
PROFANE_WORDS = [
    "expletive1", "expletive2", "inappropriate_word", "offensive_term",
    "vulgar_phrase", "offensive_language", "curse_word1", "curse_word2",
    "profanity3", "obscene_term", "vulgar_expression", "offensive_slang",
    "swear_word1", "swear_word2"
]

def check_for_profanity(text):
    return any(word in text.lower() for word in PROFANE_WORDS)

def filter_unsafe_content(text):
    if check_for_profanity(text):
        return (
            "We apologize, but we cannot display content that may be offensive.\n"
            "Let's get back on track. Could you tell us more about your recent experience?"
        )
    return text

def save_to_json(data, user_name):
    filename = f"{user_name.replace(' ', '_')}.json"
    filepath = os.path.join("response", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def delete_user_file(user_name):
    filename = f"{user_name.replace(' ', '_')}.json"
    filepath = os.path.join("response", filename)
    if os.path.exists(filepath):
        os.remove(filepath)

# Initialize session
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "survey_started" not in st.session_state:
    st.session_state.survey_started = False

# background image
image_path = "amazon.jpg"  
encoded_image = get_base64_encoded_image(image_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# form
if not st.session_state.survey_started:
    st.title("🛍️ Conversational Survey Assistant")
    st.markdown("Before we start, please share your details.")

    with st.form("user_details"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Start Survey")

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if submitted:
            if not name:
                st.warning("Please enter your name.")
            elif not re.match(email_pattern, email):
                st.warning("Please enter a valid email address (e.g., yourname@example.com).")
            else:
                st.session_state.user_info = {
                    "name": name,
                    "email": email,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.survey_started = True
                st.success(f"Welcome, {name}! Let's begin the survey.")

# Survey interface
if st.session_state.survey_started:
    st.title("🛍️ Conversational Survey Assistant")
    st.markdown("Tell us about your experience with our e-commerce website.")

    # Clear Chat
    if st.button("Clear Responses ❌"):
        delete_user_file(st.session_state.user_info.get("name", ""))
        st.session_state.user_info = {}
        st.session_state.chat_history = []
        st.session_state.survey_started = False
        st.rerun()

    user_input = st.text_input("You:", key="input_box")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        if user_input.lower() == "exit":
            st.markdown("**AI:** Thank you for your time. Have a great day! 👋")
        else:
            system_prompt = (
                "You are an AI assistant designed to conduct a conversational customer feedback survey for an e-commerce website. "
                "Your goal is to engage users in a natural, polite, and informative dialogue. Start by acknowledging their input, "
                "then ask a thoughtful follow-up or survey question that helps uncover detailed insights about their experience. "
                "Avoid generic questions—make them specific to the user's previous messages. Keep the tone friendly, concise, and respectful. "
                "Do not use any language that could be considered offensive or inappropriate."
            )

            messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )

            ai_message = response.choices[0].message.content.strip()
            ai_message = filter_unsafe_content(ai_message)

            st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
            st.markdown(f"**AI:** {ai_message}")

            # Save conversation to JSON
            user_data = {
                "user": st.session_state.user_info,
                "conversation": st.session_state.chat_history
            }
            save_to_json(user_data, st.session_state.user_info["name"])

    # Shows history
    if st.session_state.chat_history:
        st.markdown("### Conversation History")
        for entry in st.session_state.chat_history:
            st.markdown(f"**{entry['role'].capitalize()}:** {entry['content']}")