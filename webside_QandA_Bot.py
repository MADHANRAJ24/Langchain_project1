import streamlit as st
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

llm=GoogleGenerativeAI(model="gemini-2.0-flash")

def scripe_webside(url):
    loader=AsyncHtmlLoader([url])
    docs=loader.load()
    return docs

def answer_question(question,docs):
    prompt=ChatPromptTemplate.from_messages([
        ("system","""                
         
        you  are  a helpful assistant that answers questions based only on the following scraped content .
        if you don't know the answer ,say "this information is not available in the scraped data."

         scraped content:
         {content}   

        """),("human",(question))
    ])

    chain=prompt|llm

    responce=chain.invoke({"content":docs,"question":question})

    return responce

st.set_page_config("webside QandA Bot")
st.title("webside QandA Bot")
url=st.text_input("Enter URL:")

if url:
    if "current_url" not in st.session_state or st.session_state.current_url !=url:
        st.session_state.docs=scripe_webside(url)

        st.session_state.current_url=url

        st.success("Webside Scraped")

    question=st.text_input("Ask your question")

    if question and 'docs' in st.session_state:

        answer=answer_question(question,st.session_state.docs)
        st.success(answer)
    