import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import ArxivRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)

llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

st.title("Arxiv QandA bot")

with st.sidebar:
    st.header("setting")
    arxiv_code=st.text_input("Enter arxiv code")
    load_bottom=st.button("Load paper")

if "paper_loaded" not in st.session_state:
    st.session_state.paper_loaded=False
    st.session_state.retriver=None

if load_bottom and arxiv_code:
    with st.spinner("loading paper..."):
        retriver=ArxivRetriever(load_max_socs=1,doc_ids=[arxiv_code],get_full_document=True)
        docs=retriver.invoke(arxiv_code)

        st.session_state.retriver=retriver
        st.session_state.paper_loaded=True
        st.success("paper loaded")

if st.session_state.paper_loaded:
    st.divider()
    st.header("Ask question")
    question=st.text_input("Enter the question")

    if question:
        with st.spinner("Thinking..."):
            prompt=ChatPromptTemplate.from_template(""" Answer the question based only on the the context provided.Be detailed and technical in your response

    context:{context}
    question:{question}""" )
            
            def format_docs(docs):
                return"\n\n".join(doc.page_content for doc in docs)
            chain=({"context":st.session_state.retriver |format,"question":RunnablePassthrough()}|prompt |llm|StrOutputParser())
            result=chain.invoke(question)
            st.subheader("answer")
            st.markdown(result)


