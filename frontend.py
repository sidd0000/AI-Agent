# # if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()


# #Step1: Setup UI with streamlit (model provider, model, system prompt, web_search, query)
# import streamlit as st

# st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
# st.title("AI Chatbot Agents")
# st.write("Create and Interact with the AI Agents!")

# system_prompt=st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

# MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
# MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

# provider=st.radio("Select Provider:", ("Groq", "OpenAI"))

# if provider == "Groq":
#     selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
# elif provider == "OpenAI":
#     selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

# allow_web_search=st.checkbox("Allow Web Search")

# user_query=st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

# API_URL="http://127.0.0.1:9999/chat"

# if st.button("Ask Agent!"):
#     if user_query.strip():
#         #Step2: Connect with backend via URL
#         import requests

#         payload={
#             "model_name": selected_model,
#             "model_provider": provider,
#             "system_prompt": system_prompt,
#             "messages": [user_query],
#             "allow_search": allow_web_search
#         }

#         response=requests.post(API_URL, json=payload)
#         if response.status_code == 200:
#             response_data = response.json()
#             if "error" in response_data:
#                 st.error(response_data["error"])
#             else:
#                 st.subheader("Agent Response")
#                 st.markdown(f"**Final Response:** {response_data}")



import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Set page configuration (only once and at the very beginning)
st.set_page_config(page_title="LangGraph Agent UI", page_icon="🤖", layout="wide")

# Constants
API_URL = "http://127.0.0.1:9999/chat"
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

# Load and display custom CSS for styling
def local_css():
    st.markdown(
        """
        <style>
        /* App background gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #FFFFFF;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        /* Text area styling */
        .stTextArea>div>div>textarea {
            border-radius: 8px;
            border: 2px solid #334e68;
            padding: 0.75rem;
        }
        /* Button styling */
        .stButton>button {
            background-color: #334e68;
            color: #FFFFFF;
            border-radius: 20px;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #527a9f;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Utility to load Lottie animations from URL
def load_lottie(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Main app
def main():
    # Apply CSS
    local_css()

    # Header animation
    lottie_header = load_lottie("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")
    if lottie_header:
        st_lottie(lottie_header, height=150)

    st.title("🤖 AI Chatbot Agents")
    st.write("Create and Interact with your AI Agents in a sleek, modern UI!")

    # Setup sidebar controls
    with st.sidebar:
        st.header("Configuration")
        provider = st.radio("Provider:", ("Groq", "OpenAI"))
        if provider == "Groq":
            model_name = st.selectbox("Groq Model:", MODEL_NAMES_GROQ)
        else:
            model_name = st.selectbox("OpenAI Model:", MODEL_NAMES_OPENAI)
        allow_search = st.checkbox("Allow Web Search")
        st.markdown("---")
        st.subheader("System Prompt")
        system_prompt = st.text_area("", height=100, placeholder="Type your system prompt here...")

    # Layout: two columns
    col_query, col_response = st.columns([1, 2])

    # User query input
    with col_query:
        st.subheader("🔍 Your Query")
        user_query = st.text_area("", height=200, placeholder="Ask anything here...")
        ask = st.button("🚀 Ask Agent!")

    # Initialize history in session state
    if 'history' not in st.session_state:
        st.session_state.history = []

    # When user asks
    if ask and user_query.strip():
        payload = {
            "model_name": model_name,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_search
        }
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", data)
            # Save to history
            st.session_state.history.append((user_query, answer))
            st.balloons()
        else:
            answer = f"Error {response.status_code}: {response.text}"
            st.session_state.history.append((user_query, answer))

    # Display conversation history
    with col_response:
        st.subheader("💬 Conversation")
        if st.session_state.history:
            for idx, (qry, ans) in enumerate(reversed(st.session_state.history)):
                st.markdown(f"**You:** {qry}")
                st.markdown(f"**Agent:** {ans}")
        else:
            st.info("No queries yet. Ask something to get started!")

if __name__ == "__main__":
    main()

