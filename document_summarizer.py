import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import PyPDF2
import docx


load_dotenv(override=True)

llm=ChatGroq(model="llama-3.1-8b-instant")

st.title("Document Summarizer")
st.set_page_config("doct summarizer Bot")

upload_file=st.file_uploader("Choose a file",type=["pdf","docx","txt"])

summary_len=st.radio("select summary length ",("short","Medium","Long"),horizontal=True)

def extract_text_file(upload_file):
    file_extention=upload_file.name.split(".")[-1].lower()
    text=""

    if file_extention=="pdf":
        pdf_reader=PyPDF2.PdfReader(upload_file)
        for page in pdf_reader.page:
            text+=page.extract_text()
    elif file_extention=="txt":
        text=upload_file.read().decode('utf-8')

    elif file_extention=="docx":
        doc=docx.Document(upload_file)
        text="\n".join([para.text for para in doc.paragraphs])
    return text

def generate_summary(text,length):
     
     summary_length={
         "sort":"write 1-2 lines",
         "medium":"write 5-6 lines",
         "Long":"write detailed paragraph"

     }
     prompt=ChatPromptTemplate.from_tampalte(f"""
summarize the following text{summary_length[length]}.
focus on key points and main ideas.Be concise and clear.

Text:{text}
     
     
     """
     )

     chain=prompt|llm|StrOutputParser()
     return chain.invoke({'text':text})

if upload_file:
    extracted_text=extract_text_file(upload_file)

    if extracted_text:
        summary=generate_summary(extracted_text,summary_length)

        st.subheater("summary")
        st.write(summary)





