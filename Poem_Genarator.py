import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import re

load_dotenv(override=True)

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

prompt=ChatPromptTemplate.from_messages([
    ("system","""you are a genius. create a poem that strictly follows these rules:
     1.Theme:{theme}
     2.Rhyme scheme:{rhyme_scheme}
     3.Mood:{mood}

     Guidelines:
     -maintain exactly the specified rhyme scheme pattern
     -use 4 lines per stanza (unless rhyme scheme specifies otherwise)
     -Ensure natural flow and meter
     -Avoid forced rhymes
     -Include vivid imagery

     format the poem with line breaks and stanza separation 
     add emojis recived to the theme at the end."""),
     ("human","create a poem about {theme} with {rhyme_scheme} rhyme scheme.")

])
st.set_page_config("AI poem generator")

st.title("AI POEM GENERATOR")

theme=st.text_input("Enter the poem theme ")
rhyms_scheme=st.text_input("Enter the rhyms scheme").upper()
mood=st.selectbox("select mood",['joyful','romantic','mysterious','netural'])

def validate_rhymes_schems(schemes):
    if not re.match(r"^[A-Z]+$",schemes):
        return False
    return True
if not validate_rhymes_schems(rhyms_scheme):
    st.error("Invalied rhymes scheme!")
    st.stop()

if st.button("Generate Poem"):
    with st.spinner("Loading"):
        chain=prompt|llm
        responce=chain.invoke({
            "theme":theme,
            "rhyme_scheme":rhyms_scheme,
            "mood":mood
        }
        )
        st.subheader("here's your poem")
        st.markdown(responce.content)
        

