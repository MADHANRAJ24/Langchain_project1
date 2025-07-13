import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os

load_dotenv(override=True)

def get_pdf_file(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    chunks = text_splitter.split_text(text)
    return chunks

def vector_stores(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_data")

def conversational_chain():
    prompt_template = """
Answer the question as detailed as possible from the provided context and your own knowledge. 
If you do not know the answer, say you do not know.
Context:\n{context}\n
Question:\n{question}\n
Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_data", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply:", response["output_text"])

def main():
    st.set_page_config(page_title="Chat PDF")
    st.title("PDF Q&A BOT")
    st.header("Interactive RAG-based LLM Multi-PDF Document Analysis", divider="rainbow")

    user_question = st.text_input("Ask a question from the PDF files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDF files and click Submit", accept_multiple_files=True)

        if st.button("Submit"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_file(pdf_docs)
                    chunks = text_chunks(raw_text)
                    vector_stores(chunks)
                    st.success("Done")
            else:
                st.warning("Please upload at least one PDF file.")

if __name__ == "__main__":
    main()
