import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_URL", "https://chatbot-backend-3zui.onrender.com/chat")

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #f0f4f9;
        }
        .main-title {
            text-align: center;
            color: #2E86C1;
            font-size: 40px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #5D6D7E;
        }
        .response-box {
            background-color: #E8F6F3;
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid #1ABC9C;
            font-size: 16px;
        }
        .error-box {
            background-color: #FDEDEC;
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid #E74C3C;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<h1 class="main-title">🤖 AI Chatbot Agents</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create and Interact with Smart AI Agents powered by Groq & OpenAI 🚀</p>', unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.header("⚙️ Agent Settings")

system_prompt = st.sidebar.text_area(
    "📝 Define System Prompt",
    height=100,
    placeholder="Type your system prompt here..."
)

provider = st.sidebar.radio("🌐 Select Provider:", ("Groq", "OpenAI"))

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

if provider == "Groq":
    selected_model = st.sidebar.selectbox("🤖 Groq Models:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.sidebar.selectbox("🤖 OpenAI Models:", MODEL_NAMES_OPENAI)

allow_web_search = st.sidebar.checkbox("🔍 Enable Web Search")

# Main Chat Section
st.markdown("### 💬 Ask Your AI Agent")
user_query = st.text_area("Enter your query:", height=150, placeholder="Ask me anything!")

if st.button("✨ Ask Agent"):
    if user_query.strip():
        with st.spinner("🤔 Thinking..."):
            # Define payload correctly before try block
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search,
            }

            try:
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    response_data = response.json()

                    if isinstance(response_data, dict) and "error" in response_data:
                        st.markdown(
                            f'<div class="error-box">⚠️ {response_data["error"]}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        # Handle different response formats safely
                        if isinstance(response_data, str):
                            final_text = response_data
                        elif isinstance(response_data, dict) and "response" in response_data:
                            final_text = response_data["response"]
                        elif isinstance(response_data, dict) and "messages" in response_data:
                            final_text = response_data["messages"][-1]["content"]
                        else:
                            final_text = str(response_data)

                        st.markdown('<h4 style="color:#117A65;">✅ Agent Response</h4>', unsafe_allow_html=True)
                        st.write(final_text)
                else:
                    st.markdown(
                        '<div class="error-box">❌ Error: Backend not reachable</div>',
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.markdown(
                    f'<div class="error-box">Request failed: {e}</div>',
                    unsafe_allow_html=True
                )
