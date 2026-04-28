import json
import logging
from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)

async def fix_resume_ai(resume_json: dict, job_desc: str, missing_keywords: list, issues: list):
    """
    Uses LLM to automatically improve a resume based on ATS feedback (Async).
    """
    prompt = f"""
    You are an expert resume optimization engine. Your goal is to improve the candidate's resume to achieve a higher ATS score while maintaining 100% integrity.
    
    TASK:
    Improve the provided resume based on the job description and the identified gaps.
    
    CONSTRAINTS:
    - TRUTHFULNESS: Do not invent new roles, companies, or years of experience.
    - KEYWORD INJECTION: Naturally weave missing keywords into the summary, skills, and bullet points only where relevant to the user's existing background.
    - BULLET ENHANCEMENT: Transform weak descriptions into impact-oriented bullet points using action verbs and (estimated) metrics.
    - CLARITY: Improve the flow and professional tone of the summary.

    MISSING KEYWORDS TO INTEGRATE:
    {", ".join(missing_keywords[:15])}
    
    STRUCTURAL ISSUES TO FIX:
    {", ".join(issues)}

    ORIGINAL RESUME (JSON):
    ---
    {json.dumps(resume_json, indent=2)}
    ---

    TARGET JOB DESCRIPTION:
    ---
    {job_desc}
    ---

    OUTPUT FORMAT:
    Return ONLY the improved resume as a JSON object in the exact same structure as the original.
    """

    try:
        response = await llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a professional resume optimization agent. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        logger.error(f"Resume Fixer Error: {e}")
        return resume_json
