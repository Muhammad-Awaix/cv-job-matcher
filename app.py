import streamlit as st
from prompts import get_analysis_prompt, validate_description, get_cover_letter_prompt
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os

load_dotenv()

# define llm ONCE at the top
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key
)
st.sidebar.divider()
st.sidebar.title("Built by")
st.sidebar.write("Muhammad Awais")
st.sidebar.markdown("[GitHub](https://github.com/Muhammad-Awaix)")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/muhamad-awaix)")
st.sidebar.markdown("[Email](mailto:mawais.ai021@gmail.com)")
st.sidebar.title("How to use")
st.sidebar.write("1. Upload your CV in PDF format")
st.sidebar.write("2. Paste the job description")
st.sidebar.write("3. Click Analyze")
st.sidebar.write("4. Get your score and cover letter")

st.title("CV Analyzer with Groq LLM")
st.subheader("Paste a job description and get your CV scored instantly")

uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")
job_description = st.text_area("Enter the job description here:", height=200)

if st.button("Analyze"):
    if uploaded_file is None or not job_description:
        st.warning("Please upload your CV and paste a job description first")
    else:
        with st.spinner("Validating job description..."):
            validation_prompt = validate_description(job_description)
            validation_response = llm.invoke([HumanMessage(content=validation_prompt)])
            is_valid = validation_response.content.strip().upper()

        if is_valid == "NO":
            st.error("This doesn't look like a job description. Please enter a valid one.")
        else:
            with st.spinner("Analyzing your CV..."):
                # save uploaded file to disk first
                with open("temp_cv.pdf", "wb") as f:
                    f.write(uploaded_file.read())

                loader = PyPDFLoader("temp_cv.pdf")
                doc = loader.load()
                cv_text = doc[0].page_content

                prompt = get_analysis_prompt(cv_text, job_description)
                response = llm.invoke([HumanMessage(content=prompt)])
                st.markdown(response.content)

                st.session_state["cv_text"] = cv_text
                st.session_state["analysis_done"] = True
if st.session_state.get("analysis_done"):
    st.divider()
    if st.button("Generate Cover Letter"):
        with st.spinner("Writing your cover letter..."):
            from prompts import get_cover_letter_prompt
            cover_prompt = get_cover_letter_prompt(
                st.session_state["cv_text"],
                job_description
            )
            cover_response = llm.invoke([HumanMessage(content=cover_prompt)])
            st.markdown(cover_response.content)