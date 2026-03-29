import streamlit as st
from prompts import get_analysis_prompt
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os

load_dotenv()

st.title("CV Analyzer with Groq LLM")
st.subheader("Paste a job description and get your CV scored instantly")

# BOTH inputs must be OUTSIDE the button
uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")
job_description = st.text_area("Enter the job description here:", height=200)

if st.button("Analyze"):
    if uploaded_file is None or not job_description:
        st.warning("Please upload your CV and paste a job description first")
    else:
        with st.spinner("Analyzing your CV..."):
            with open("temp_cv.pdf", "wb") as f:
                f.write(uploaded_file.read())

            loader = PyPDFLoader("temp_cv.pdf")
            doc = loader.load()
            cv_text = doc[0].page_content

            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=os.getenv("GROQ_API_KEY")
            )

            prompt = get_analysis_prompt(cv_text, job_description)

            response = llm.invoke([HumanMessage(content=prompt)])
            st.markdown(response.content)