import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gpt
from functions import*

# load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Learn with Study Engine",
    page_icon=":brain:",  # Favicon emoji
    layout="wide",  # Page layout option
    initial_sidebar_state="collapsed"
)

# visual style 
st.markdown("""
<style>
    /* Change the color of the chat input border and focus */
    .stTextInput>div>div>input:focus {
        border-color: #5880b9; /* A professional blue */
        box-shadow: 0 0 0 0.2rem rgba(88, 128, 185, 0.25);
    }
    /* Hide the 'Made with Streamlit' footer */
    footer {visibility: hidden;}
    /* Tweak the main page padding for better spacing */
    .main { padding-top: 2rem; } 
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini AI model
if not API_KEY:
    st.error("Error: GOOGLE_API_KEY environment variable not found.")
    st.stop() # Stop the app if no key is found

gpt.configure(api_key=API_KEY)
model = gpt.GenerativeModel('gemini-2.5-flash')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Use a container for the header to give it structure
with st.container():
    st.markdown("<h1 style='text-align: center; color: #1e81b0;'>🤖 Learn with Study Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Your AI tutor for personalized and fast learning.</p>", unsafe_allow_html=True)
    st.markdown("---") # A separator line for a cleaner break


# Chat history is displayed normally
for msg in st.session_state.chat_session.history:
    # map_role is assumed to be in functions.py (e.g., user -> user, model -> assistant)
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Study Engine...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to Gemini and get the response
    # fetch_gemini_response is assumed to be in functions.py
    gemini_response = fetch_gemini_response(user_input)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Update chat history
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})