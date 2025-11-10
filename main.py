from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from extract_file import extract_text_from_file


def generate_response(uploaded_file, openai_api_key, query_text):
    documents = []
    # Load document if file is uploaded
    if uploaded_file is not None:
        for file in uploaded_file:
            text = extract_text_from_file(file)
            if text.strip():  # avoid empty docs
                documents.append(text)

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(
            api_key=openai_api_key,
            model="text-embedding-3-small"
        )

        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever(search_kwargs={"k": 3})

        llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",
            max_tokens=512,
            temperature=0
        )

        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=retriever
        )
        return qa.run(query_text)
    return None
