def validate_description(description):
    return f"""
Is the following text a valid job description? 
Reply with only YES or NO. Nothing else.

Text:
{description}
"""
def get_analysis_prompt(cv_text, job_description):
    return f"""
You are an expert career coach. Analyze the CV against the job description below.

Structure your response exactly like this:

## Match Score: X/10

## Why This Score
2-3 sentences explaining the score honestly.

## Your Strongest Matches
- List the skills/experiences that directly match the job
- Be specific, not generic

## Critical Gaps
- List what's missing or weak compared to the job requirements
- Be honest, not harsh

## How To Improve Your CV For This Role
- Concrete, actionable suggestions only
- No fluff

CV:
{cv_text}

Job Description:
{job_description}
"""

def get_cover_letter_prompt(cv_text, job_description):
    return f"""
Write a professional tailored cover letter based on the CV and job description below.
Use the candidate's actual projects and skills. 
Start with "Dear Hiring Manager".
Keep it under 300 words.

CV:
{cv_text}

Job Description:
{job_description}
"""