import streamlit as st
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

            prompt = f"""
            You are a career advisor. Given the CV and job description below, do three things:
            1. Score the CV against the job description out of 10.
            2. Highlight the most relevant skills and experiences from the CV.
            3. Provide suggestions for improving the CV to better match the job description.

            CV:
            {cv_text}

            Job Description:
            {job_description}
            """

            response = llm.invoke([HumanMessage(content=prompt)])
            st.markdown(response.content)