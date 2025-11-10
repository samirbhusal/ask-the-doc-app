import streamlit as st

from handle_key import get_api_key
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


with st.form('myform'):
    openai_api_key = get_api_key(uploaded_file, query_text)
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key:
            st.error("Please provide an OpenAI API key.")
        else:
            with st.spinner("Calculating..."):
                try:
                    response = generate_response(uploaded_file, openai_api_key, query_text)
                    st.info(response["result"])
                except Exception as e:
                    st.error(f"Error: {str(e)}")