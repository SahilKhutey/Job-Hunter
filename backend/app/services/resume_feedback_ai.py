import json
from app.ai.llm_client import llm_client

async def generate_resume_feedback(resume_text: str, job_desc: str, missing_keywords: list):
    """
    Uses AI to provide qualitative feedback on resume-job alignment (Async).
    """
    prompt = f"""
    You are an expert recruiter and ATS specialist. 
    Analyze the resume against the job description and provide actionable feedback.
    
    JOB DESCRIPTION:
    {job_desc}
    
    MISSING KEYWORDS:
    {", ".join(missing_keywords[:15])}
    
    RESUME TEXT:
    {resume_text}
    
    Return a structured JSON with:
    - strengths: list of strings (what the user does well)
    - weaknesses: list of strings (where the gaps are)
    - improvements: list of strings (specific, actionable advice)
    """

    try:
        res = await llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a specialized career coach and ATS auditor. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = res.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception:
        return {
            "strengths": ["Clear formatting", "Includes relevant contact info"],
            "weaknesses": ["Keyword gaps", "Generic descriptions"],
            "improvements": ["Add more technical keywords", "Quantify bullet points"]
        }
