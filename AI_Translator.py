import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)
llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")
prompt=ChatPromptTemplate.from_messages([("system","you are a helpfull assistent that translates{input_language}to{output_language}"),("human","{input}"),])

st.set_page_config("AI Translator")
st.title("AI Translator")

input_lang=st.text_input("input language")
output_lang=st.text_input("output language")

input_text=st.text_input("Text to Traslate")

if st.button("Translate "):
    if input_lang.strip() and output_lang.strip() and input_text.strip():
        chain=prompt|llm

        responce=chain.invoke({
            "input_language":input_lang,
            "output_language":output_lang,
            "input":input_text
        })
        
        st.write(responce.content)

    else:
        st.warning("Fill the all colum than click the Translate button")
else:
    st.info("Fill the all colum than click the Translate button")


