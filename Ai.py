from dotenv import load_dotenv
import os
from google import genai
import streamlit as st

st.set_page_config("AI Recipe Genarator Bot")
load_dotenv(override=True)

GEMINI_API=os.getenv("GEMINI_API")

client=genai.Client(api_key=GEMINI_API)

st.title("AI Recipe Genarator")

ingredients=st.text_area("Ingredients")

if st.button("Generate Recipe"):
    if ingredients:
          
          prompt=f"Give me a recipe with p{ingredients}"
          responce=client.models.generate_content(model="gemini-2.0-flash",contents=prompt)
          st.markdown(responce.text)
    else:
         st.warning("Enter the ingredients")
         
        




