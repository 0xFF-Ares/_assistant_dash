import streamlit as st
from utils.utils import query_ollama, list_models


st.title("📝 File Q&A")
st.session_state.messages  = []

with st.sidebar:
    st.header("Settings")
    
    st.subheader("Model")
    model_type = st.selectbox("Model Type", ["Offline", "Online"], index=0)

    if model_type == "Offline":
        st.session_state["model_name"] = st.selectbox("Choose a model", list_models(), index=0 if list_models() else None)
        st.session_state["temperature"] = st.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
        st.session_state["system_prompt"] = st.text_area("System Prompt", "", help="Set an initial system instruction for the model.")
    elif model_type == "Online":
        import anthropic
        anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

uploaded_file = st.file_uploader("Upload a file for analysis")

if model_type == "Online":
        question = st.text_input(
            "Ask something about the article",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )
        if not anthropic_api_key:
            st.info("Please add your Anthropic API key to continue.")
            st.stop()
        else:
            article = uploaded_file.read().decode()
            prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
            {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

            client = anthropic.Client(api_key=anthropic_api_key)
            response = client.completions.create(
                prompt=prompt,
                stop_sequences=[anthropic.HUMAN_PROMPT],
                model="claude-v1",  # "claude-2" for Claude 2 model
                max_tokens_to_sample=100,
            )
            st.write("### Answer")
            st.write(response.completion)

if model_type == "Offline":
    if question := st.chat_input(disabled=not uploaded_file):
        st.session_state.messages = []
        st.chat_message("user").write(question)

        prompt = f"""Analyze this file and answer the following question, if there is no question then just 
        provide an analysis: {uploaded_file.read().decode('utf-8')} \n {question}"""

        file_content = uploaded_file.read().decode("utf-8")
        response = query_ollama(prompt, model=st.session_state.get("model_name", "default"), temperature=st.session_state.get("temperature", 0.7), system_prompt=st.session_state.get("system_prompt", ""))
        st.chat_message("assistant").write(response)