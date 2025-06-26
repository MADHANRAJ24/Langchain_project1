import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

st.title("AI Splling and Gramer checker")

Prompt_Template=PromptTemplate(input_variables=["text"],template="""
analyze the following text for spelling and grammar errors.provide:
1.correct text
2.list of the erro found (if any)
3.Explanation of corrections

text:{text}

format your response as follows
**correct text**
[correct text here]
**Errors Found**
-[error1]:[explanation]
-[error2]:[explanation]

**Explanation:**
[general explanation of correction]
"""
)


user_input=st.text_area("Enter your text")

if st.button("check test"):
    chain=LLMChain(llm=llm,prompt=Prompt_Template)
    result=chain.run(text=user_input)
    st.markdown(result)
