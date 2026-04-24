import json
import logging
from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)

def parse_resume_to_json(text: str):
    """
    Uses LLM to transform raw resume text into a structured profile schema.
    """
    prompt = f"""
    You are an expert recruitment AI. Analyze the following raw resume text and extract structured information into a precise JSON format.
    
    Expected JSON Schema:
    {{
        "full_name": "string",
        "email": "string",
        "phone": "string",
        "location": "string",
        "job_title": "string",
        "summary": "string",
        "skills": ["string"],
        "experience": [
            {{
                "company": "string",
                "role": "string",
                "duration": "string",
                "description": "string"
            }}
        ],
        "education": [
            {{
                "institution": "string",
                "degree": "string",
                "year": "string"
            }}
        ],
        "links": {{
            "linkedin": "string",
            "github": "string",
            "portfolio": "string"
        }}
    }}

    If a field is missing, use an empty string or empty list. Do not hallucinate.

    Resume Text:
    ---
    {text}
    ---

    Return ONLY the JSON object.
    """

    try:
        # Using the existing llm_client if available, otherwise fallback to direct openai
        # Assuming llm_client has a method for general completion
        response = llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a specialized resume parsing engine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        # Clean the response string if it contains markdown code blocks
        content = response.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        logger.error(f"Failed to parse resume with AI: {e}")
        return {
            "full_name": "",
            "email": "",
            "phone": "",
            "location": "",
            "job_title": "",
            "skills": [],
            "experience": [],
            "education": [],
            "links": {}
        }
