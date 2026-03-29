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

## Tailored Cover Letter
Write a professional, personalized cover letter using the candidate's
actual projects and skills. Do not use placeholder text like [Company Name].
Write "Dear Hiring Manager" instead.

CV:
{cv_text}

Job Description:
{job_description}
"""