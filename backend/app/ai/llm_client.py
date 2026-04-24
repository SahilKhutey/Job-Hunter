from openai import OpenAI
from app.core.config import settings
from typing import Dict, Any, List
import json

EXTRACTION_PROMPT = """
Extract structured information from this resume.
Return JSON with:
- full_name
- email
- phone
- skills
- education (list)
- experience (list of dicts with role, company, duration, description)
- projects (list of dicts with name, description, tech)
- links (linkedin, github, portfolio)
Resume:
{resume_text}
"""

JOB_ANALYST_PROMPT = """
Analyze the following job description and extract key structured data.
Return JSON with:
- title
- company
- skills_required (list)
- experience_required (string)
- location (string or "Remote")
- type (string)
- key_responsibilities (list)
- seniority_level (string)
- tone (string e.g. "startup", "corporate")
Job Description:
{job_description}
"""

RESUME_REWRITE_PROMPT = """
You are an expert resume writer.
Rewrite the resume to match the job.
RULES:
- Keep it truthful
- Use action verbs
- Add metrics if possible
- Include job keywords naturally
- Optimize for ATS
USER PROFILE:
{profile}
JOB DESCRIPTION:
{job}
OUTPUT:
Structured JSON:
- summary (string)
- skills (list)
- experience (rewritten bullets)
- projects (rewritten)
"""

BULLET_ENHANCE_PROMPT = """
Improve this resume bullet:
{bullet}
Add:
- impact
- metrics
- strong verbs
Return ONLY the improved bullet string.
"""

COMPANY_CONTEXT_PROMPT = """
Extract company mission, culture, and values from the following text:
{text}
Return JSON with:
- mission (string)
- culture (string)
- tech_stack (list)
"""

POSITIONING_PROMPT = """
Based on the profile and job, define how the user should be positioned.
PROFILE: {profile}
JOB: {job}
Return JSON with:
- positioning (string)
- strengths (list)
- angle (string)
"""

COVER_LETTER_PROMPT = """
Write a concise, strong cover letter.
RULES:
- 200–300 words
- No fluff
- Specific to job
- Mention company
- Highlight relevant skills
- Sound human, not generic
PROFILE:
{profile}
JOB:
{job}
POSITIONING:
{positioning}
OUTPUT:
Cover letter text only.
"""

FORM_ANSWER_PROMPT = """
Generate professional answers for job application questions.
RULES:
- Be concise (2–5 lines)
- Be specific to job
- Avoid generic answers
- Keep tone confident
PROFILE:
{profile}
JOB:
{job}
QUESTIONS:
{questions}
OUTPUT:
JSON:
[
  {"question": "...", "answer": "..."}
]
"""

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _call_json(self, prompt: str, system_msg: str) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error parsing JSON from LLM: {e}")
            return {}

    def _call_text(self, prompt: str, system_msg: str, temperature: float = 0.5) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error from LLM text generation: {e}")
            return ""

    def get_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    # Existing methods

    def extract_profile_data(self, resume_text: str) -> Dict[str, Any]:
        return self._call_json(EXTRACTION_PROMPT.format(resume_text=resume_text), "You are an expert data extraction tool. Always return valid JSON.")

    def analyze_job(self, job_description: str) -> Dict[str, Any]:
        return self._call_json(JOB_ANALYST_PROMPT.format(job_description=job_description), "You are an expert Job Analyst Agent. Always return valid JSON.")

    # Resume Engine methods
    def rewrite_resume(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        return self._call_json(RESUME_REWRITE_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job)), "You are an expert resume optimizer. Always return valid JSON.")

    def enhance_bullet(self, bullet: str) -> str:
        return self._call_text(BULLET_ENHANCE_PROMPT.format(bullet=bullet), "You are a professional resume writer.", temperature=0.7)

    # Application Generator methods
    def extract_company_context(self, text: str) -> Dict[str, Any]:
        return self._call_json(COMPANY_CONTEXT_PROMPT.format(text=text), "You are a company intelligence analyst. Always return valid JSON.")

    def generate_positioning(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        return self._call_json(POSITIONING_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job)), "You are a strategic career advisor. Always return valid JSON.")

    def generate_cover_letter(self, profile: Dict[str, Any], job: Dict[str, Any], positioning: Dict[str, Any] = None) -> str:
        # Backward compatibility for older code without positioning
        pos = json.dumps(positioning) if positioning else "N/A"
        return self._call_text(COVER_LETTER_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job), positioning=pos), "You are an elite career consultant.", temperature=0.7)

    def generate_form_answers(self, profile: Dict[str, Any], job: Dict[str, Any], questions: List[str]) -> List[Dict[str, str]]:
        res = self._call_json(FORM_ANSWER_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job), questions=json.dumps(questions)), "You are an expert job application assistant. Always return valid JSON.")
        # Sometimes the LLM nests the array under a key like "answers"
        if isinstance(res, dict):
            for k, v in res.items():
                if isinstance(v, list):
                    return v
        return []

llm_client = LLMClient()
