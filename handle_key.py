import streamlit as st
import os


def get_api_key(uploaded_file, query_text):
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key
    elif "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    else:
        return st.text_input(
            "OpenAI API Key",
            type="password",
            disabled=not (uploaded_file and query_text)
        )
