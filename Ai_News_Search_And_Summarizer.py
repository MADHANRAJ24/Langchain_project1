import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from dotenv import load_dotenv
import os 

load_dotenv(override=True)

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

st.set_page_config("Ai news search and summarizer")

st.title("AI news search & summarizer")

search_news=st.text_input("Enter your search term")

cal1,cal2=st.columns(2)

with cal1:
    region=st.selectbox("Region",["us-en","uk-en","fr-fr"],index=0)

with cal2:
    time_range=st.selectbox("Time",["d","W","m"],index=0)


if st.button("search"):
    wrapper=DuckDuckGoSearchAPIWrapper(
                region=region,
                time=time_range,
                max_results=5)

    search=DuckDuckGoSearchResults(api_wrapper=wrapper,source="news")
    result=search.invoke(search_news)

    with st.expander("Raw news"):
        st.write(result)

    prompt=f"""
    please summarize the following news search result'{search_news}'
    into a concise paragraph.Include the most relevent the responce with markdown for better readability

    search result:
    {result}

    """
    with st.spinner("Genarating..."):
        summary=llm.invoke(prompt)

    st.subheader("News Summary")
    st.markdown(summary.content)


    