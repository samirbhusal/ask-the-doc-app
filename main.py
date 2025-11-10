from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from extract_file import extract_text_from_file


def generate_response(uploaded_file, openai_api_key, query_text):
    documents = []

    if uploaded_file:
        # Extract text from each file
        for file in uploaded_file:
            text = extract_text_from_file(file)
            if text.strip():
                documents.append(text)

        # Split into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.create_documents(documents)

        # Embeddings
        embeddings = OpenAIEmbeddings(
            api_key=openai_api_key,
            model="text-embedding-3-small"
        )

        # Vector store
        db = Chroma.from_documents(texts, embeddings)

        # Retriever
        retriever = db.as_retriever(search_kwargs={"k": 3})

        # LLM
        llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",
            max_tokens=512,
            temperature=0
        )

        # QA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

        return qa.invoke(query_text)

    return None