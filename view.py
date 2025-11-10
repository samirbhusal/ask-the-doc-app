import os
import streamlit as st

from main import generate_response

# Page title
st.set_page_config(page_title='🦜🦜 Ask the Doc App')
st.title('🦜🦜 Ask the Doc App')
# File upload
uploaded_file = st.file_uploader('Upload an article', type=['txt', 'pdf', 'docx'],
                                 accept_multiple_files=True)

# Query text
query_text = st.text_input('Enter your question:', placeholder='Please provide a short summary.',
                           disabled=not uploaded_file)

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else None
    if not openai_api_key:
        openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled=not (uploaded_file and query_text))
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)
            del openai_api_key
            if len(result):
                st.info(response)
