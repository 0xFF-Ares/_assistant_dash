import streamlit as st
from utils.utils import list_models, query_ollama
import subprocess

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

def start_ollama(model):
    # Start ollama in the background
    subprocess.Popen(["ollama", "run", model], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if "model_name" not in st.session_state:
    st.session_state["model_name"] = list_models()[0]
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.7
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""

start_ollama(st.session_state["model_name"])

with st.sidebar:
    st.header("Settings")
    
    st.subheader("Model")
    model_type = st.selectbox("Model Type", ["Offline", "Online"], index=0)

    if model_type == "Offline":
        st.session_state["model_name"] = st.selectbox("Choose a model", list_models(), index=0 if list_models() else None)
        st.session_state["temperature"] = st.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
        st.session_state["system_prompt"] = st.text_area("System Prompt", "", help="Set an initial system instruction for the model.")
    elif model_type == "Online":
        from openai import OpenAI
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]



if prompt := st.chat_input():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if model_type == "Online":
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    elif model_type == "Offline":
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = query_ollama(prompt, model=st.session_state["model_name"], temperature=st.session_state["temperature"], system_prompt=st.session_state["system_prompt"])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)    
