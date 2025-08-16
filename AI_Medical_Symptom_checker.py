import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv(override=True)

model=ChatGroq(model="llama-3.1-8b-instant")

st.set_page_config("Medical symptom checker")

st.title("AI Medical System checker")

def possible_condition(symptoms:str)->str:
    prompt=(
        "you are a helpful medical assistent .based on the following symptoms,suggest 3-5 possible contidion or causes ."
        "Keep the explanation simple and friendly .\n\n"
        f"symptoms:{symptoms}\n\n"
        "response:"
    )

    response=model.invoke(prompt)

    return response.content.strip()
youser_symptoms=st.text_area("Descripe your symptoms")

if st.button("Check causes"):
    with st.spinner("Analysing your symptoms..."):
        result=possible_condition(youser_symptoms)
        st.write(result)

