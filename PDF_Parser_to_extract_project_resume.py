import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import PyPDF2
import io

load_dotenv(override=True)
llm=ChatGoogleGenerativeAI(model="gemni-2.0-flash")
prompt=ChatPromptTemplate.from_messages([(
    "system",
    """You are an expert resume parser.Extract only the **Projects** section from the resume.
    for each projects,provide:
    -**Project Name** (if available)
    -**Description** (Key details about the projects)
    -**Technologies used**(Programming language,tools,frameworks)
    -**Duration**(if mentioned)
    -**Key Achievements**(if any)
    Format the output in lean markdown with bullet points. skip any irrelevent information.
    if no projects are found ,say"NO Projects found in the resume."    """
),("human","{resume_text}")])

st.set_page_config("resume parser")

st.title("resume parser")

upload_files=st.file_uploader("Upload resume",type=["pdf"])
if upload_files is not None:
    pdf_reader=PyPDF2.PdfReader(io.BytesIO(upload_files.read()))
    resume_text=""
    for page in pdf_reader.pages:
        resume_text+=page.extract_text()

    if st.button("extract project"):
        chain=prompt|llm
        responce=chain.invoke({"resume_text":resume_text})

        st.subheader("Extracted project")
        st.markdown(responce.content)

    else:
        st.warning("upload the resume pdf formate ")



    
    
    