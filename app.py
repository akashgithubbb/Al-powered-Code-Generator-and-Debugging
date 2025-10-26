import streamlit as st
import time
import requests

st.set_page_config(page_title="Code Llama Assistant", page_icon="🦙", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm powered by Groq AI. Describe what code you need, and I'll generate it for you."}]

st.title("🦙 Code Generator with Groq")
st.caption("Powered by Groq AI - Free & Fast")

with st.sidebar:
    st.header("⚙️ Settings")
    st.subheader("API Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="Paste your Groq API key here")
    st.subheader("Model Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 100, 4000, 2000, 100)
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm powered by Groq AI. Describe what code you need, and I'll generate it for you."}]
        st.rerun()
    st.divider()
    st.caption("Built for AI Engineers")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def call_groq_api(prompt, api_key, temperature, max_tokens):
    if api_key:
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            payload = {
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': 'You are an expert programmer. Generate clean, efficient, and well-commented code based on user requests.'},
                    {'role': 'user', 'content': f'Write Python code for: {prompt}'}
                ],
                'temperature': temperature,
                'max_tokens': max_tokens
            }
            response = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"❌ API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    return "⚠️ **Please enter your Groq API key in the sidebar!**"

prompt = st.chat_input("Describe the code you need...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Generating code..."):
            response = call_groq_api(prompt, api_key, temperature, max_tokens)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
