from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os
load_dotenv()

# Step 1: take the document from loader
file_path = "resources/mawais resume.pdf"
loader = PyPDFLoader(file_path=file_path)
doc = loader.load()
cv_text = doc[0].page_content
# Step 2: take a job description string as input
job_description = """
We are looking for a junior AI developer with experience in 
Python, LangChain, and RAG applications. Must have deployed 
at least one LLM-based project.
"""
# Step 3: send both to Groq LLM with a prompt
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key= os.getenv('GROQ_API_KEY')
)
# Step 4: ask it to do two things:
#         - score my CV against the job (out of 10)
#         - write a tailored cover letter
prompt = f"""
You are a career advisor. Given the CV and job description below, do two things:

1. Score the CV against the job description out of 10. Explain why.
2. Write a tailored cover letter for this job based on the CV.

CV:
{cv_text}

Job Description:
{job_description}
"""

# Send to LLM
response = llm.invoke([HumanMessage(content=prompt)])

# Step 5: print the result
print(response.content)