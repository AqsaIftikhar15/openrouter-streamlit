import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in your .env file.")

# API headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 5 Free Models with Human-Like Responses
models = {
    "🧠 Mistral 7B": "mistralai/mistral-7b-instruct",
    "📘 Mixtral 8x7B": "mistralai/mixtral-8x7b-instruct",
    "🦙 LLaMA 3 8B": "meta-llama/llama-3-8b-instruct",
}

# Streamlit UI
st.title("🤖 Talk to 5 Friendly AI Models!")

user_prompt = st.text_area("💬 What's your question or topic?")

if st.button("🚀 Get Answers") and user_prompt.strip():
    for name, model_id in models.items():
        st.subheader(f"📌 {name}")
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_id,
                        "messages": [{"role": "user", "content": user_prompt}]
                    }
                )
                try:
                    reply = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Response received!")
                    st.write(reply)
                except (KeyError, IndexError):
                    st.warning("⚠️ Unexpected format. Here's the raw output:")
                    st.code(response.text)
            except Exception as e:
                st.error(f"❌ Error from {name}: {e}")
