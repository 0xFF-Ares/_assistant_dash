import streamlit as st
from langchain.prompts import PromptTemplate
from utils.utils import list_models, query_ollama

st.title("🔗 Langchain - Generator App")

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


def blog_outline(model_type, topic_type, topic):
    # Prompt
    template = "Generate an {topic_type} about {topic}."
    prompt = PromptTemplate(input_variables=["topic_type", "topic"], template=template)
    prompt_query = prompt.format(topic_type=topic_type, topic=topic)

    if model_type == 'Offline':
        response = query_ollama(
            prompt=prompt_query,
            model=st.session_state.get("model_name", "default"),
            temperature=st.session_state.get("temperature", 0.7),
            system_prompt=st.session_state.get("system_prompt", "")
        )
        return st.info(response)
    elif model_type == 'Online':
        # Instantiate LLM model
        llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)
        # Run LLM model
        response = llm(prompt_query)
        # Print results
        return st.info(response)

with st.form("myform"):
    topic_type = st.selectbox("Select topic type:", ["Blog", "Article", "Essay", "Story", "Poem", "Script"])
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if model_type == 'Offline' and submitted:
        blog_outline(model_type, topic_text)
    elif model_type == "Online":
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        else:
            blog_outline(model_type, topic_type, topic_text)
        