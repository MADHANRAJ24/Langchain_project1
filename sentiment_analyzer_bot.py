import streamlit as st

from transformers import pipeline

sentement=pipeline("sentiment-analysis")

st.set_page_config("Sentiment Analyzer")
st.title("Sentiment Analyzer Bot")

user_input=st.text_input("Enter text:")

if st.button("Get Sentiment"):
    if user_input:
        result=sentement(user_input)

        st.write(result[0]["label"])

    else:
        st.warning("Fill The input area")

