import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    api_key = st.secrets["GEMINI_API_KEY"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key,
        
    )

    return llm