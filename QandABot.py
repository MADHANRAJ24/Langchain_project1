import streamlit as st
from transformers import pipeline

pipe = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")

st.set_page_config("Question & Answering Bot")

st.title("Question & Answering Bot")

context=st.text_area("Enter The Context",height=200)
question=st.text_input("Enter Your Question")

if st.button("Get Answer"):
    if context.strip() and question.strip():
        responce=pipe(question=question,context=context)
        st.subheader("Answer:")
        st.write(responce['answer'])

    else:
        st.warning("Fill the both And get the answer")