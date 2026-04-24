import json
import logging
from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)

def tailor_resume(profile: dict, job_description: str):
    """
    Uses LLM to rewrite and reorder a candidate's profile to perfectly match a job description
    while maintaining truthfulness and ATS optimization.
    """
    prompt = f"""
    You are an elite ATS (Applicant Tracking System) optimization engine and expert recruitment consultant.
    
    TASK:
    Rewrite the provided candidate profile to be perfectly tailored for the specific job description below.
    
    GOALS:
    1. MATCH KEYWORDS: Incorporate relevant keywords from the job description into the summary and bullet points.
    2. HIGHLIGHT RELEVANCE: Reorder and emphasize experience that directly relates to the job requirements.
    3. QUANTIFY IMPACT: Ensure bullet points focus on achievements and metrics (e.g., "Increased X by Y% using Z").
    4. MAINTAIN TRUTH: Do not invent companies, fake years of experience, or add tools the user hasn't listed or hinted at.
    5. ATS OPTIMIZATION: Use clear, professional language that parsing algorithms favor.

    CANDIDATE PROFILE (JSON):
    ---
    {json.dumps(profile, indent=2)}
    ---

    JOB DESCRIPTION:
    ---
    {job_description}
    ---

    OUTPUT FORMAT:
    Return ONLY a JSON object with the following structure:
    {{
        "summary": "Tailored professional summary (3-4 lines)",
        "skills": ["Skill 1", "Skill 2", ...],
        "experience": [
            {{
                "company": "string",
                "role": "string",
                "duration": "string",
                "bullets": ["Optimized bullet point 1", "Optimized bullet point 2", ...]
            }}
        ],
        "projects": [
            {{
                "name": "string",
                "bullets": ["string"]
            }}
        ],
        "education": "string"
    }}
    """

    try:
        response = llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a professional resume tailoring agent."},
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
        logger.error(f"Tailoring Error: {e}")
        # Return original profile as fallback in matching structure
        return {
            "summary": profile.get("summary", ""),
            "skills": profile.get("skills", []),
            "experience": profile.get("experience", []),
            "projects": profile.get("projects", []),
            "education": profile.get("education", "")
        }
