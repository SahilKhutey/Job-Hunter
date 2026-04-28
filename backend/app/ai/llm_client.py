from openai import AsyncOpenAI
from app.core.config import settings
from typing import Dict, Any, List
import json
from app.utils.privacy import privacy_shield

EXTRACTION_PROMPT = """
Extract structured information from this resume.
Return JSON with:
- full_name
- email
- phone
- summary (concise professional summary)
- skills (list of strings)
- total_experience_years (number)
- top_5_skills (list)
- suggested_job_titles (list)
- education (list of dicts with degree, institute, year)
- experience (list of dicts with title, company, duration, bullets)
- projects (list of dicts with name, description, tech)
- links (linkedin, github, portfolio)
Resume:
{resume_text}
"""

JOB_ANALYST_PROMPT = """
Analyze the following job description and extract key structured data with elite recruitment intelligence.
Return JSON with:
- title
- company
- skills_required (list of strings)
- experience_required (string)
- location (string)
- type (string)
- key_responsibilities (list)
- seniority_level (string)
- tone (string)
- red_flags (list of potential concerns: e.g., "Generic Description", "Excessive Requirements", "Toxic Phrases")
- strategic_risk_score (0-100, where 100 is high risk of ghost posting or poor fit)
- priority_index (HIGH/MEDIUM/LOW based on role impact)

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

MAP_FORM_PROMPT = """
You are a browser automation expert.
Map the following browser DOM elements to the user's profile fields.

USER PROFILE:
{profile}

DOM ELEMENTS:
{elements}

Return a JSON list of actions:
[
  {"selector": "...", "action": "type", "value": "...", "reason": "..."},
  {"selector": "...", "action": "click", "reason": "...", "is_navigation": true/false},
  {"selector": "...", "action": "select", "value": "...", "reason": "..."}
]

RULES:
1. Only map 'type' or 'select' fields that clearly correspond to profile data.
2. If there are multiple navigation buttons (e.g., 'Back', 'Next', 'Continue', 'Submit', 'Apply'), choose the ONE that moves the application FORWARD.
3. Mark navigation buttons with "is_navigation": true.
4. If the page contains a "Submit" or "Apply" button and all relevant data entry fields are filled, select it.
5. If no data entry fields are found, look ONLY for navigation buttons that move forward.
"""

class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def _call_json(self, prompt: str, system_msg: str) -> Dict[str, Any]:
        try:
            clean_prompt = privacy_shield.mask_pii(prompt)
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": clean_prompt}
                ],
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return {}

    async def _call_text(self, prompt: str, system_msg: str, temperature: float = 0.5) -> str:
        try:
            clean_prompt = privacy_shield.mask_pii(prompt)

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": clean_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error from LLM text generation: {e}")
            return ""

    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """General purpose chat completion (Async)."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in chat_completion: {e}")
            return ""

    async def generate_text(self, prompt: str, system_prompt: str = "You are a helpful assistant.", temperature: float = 0.5) -> str:
        """Public method for text generation (Async)."""
        return await self._call_text(prompt, system_prompt, temperature)

    async def get_embedding(self, text: str) -> List[float]:
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    async def extract_profile_data(self, resume_text: str) -> Dict[str, Any]:
        return await self._call_json(EXTRACTION_PROMPT.format(resume_text=resume_text), "You are an expert data extraction tool. Always return valid JSON.")

    async def analyze_job(self, job_description: str) -> Dict[str, Any]:
        return await self._call_json(JOB_ANALYST_PROMPT.format(job_description=job_description), "You are an expert Job Analyst Agent. Always return valid JSON.")

    async def rewrite_resume(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_json(RESUME_REWRITE_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job)), "You are an expert resume optimizer. Always return valid JSON.")

    async def enhance_bullet(self, bullet: str) -> str:
        return await self._call_text(BULLET_ENHANCE_PROMPT.format(bullet=bullet), "You are a professional resume writer.", temperature=0.7)

    async def extract_company_context(self, text: str) -> Dict[str, Any]:
        return await self._call_json(COMPANY_CONTEXT_PROMPT.format(text=text), "You are a company intelligence analyst. Always return valid JSON.")

    async def generate_positioning(self, profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_json(POSITIONING_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job)), "You are a strategic career advisor. Always return valid JSON.")

    async def generate_cover_letter(self, profile: Dict[str, Any], job: Dict[str, Any], positioning: Dict[str, Any] = None) -> str:
        pos = json.dumps(positioning) if positioning else "N/A"
        return await self._call_text(COVER_LETTER_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job), positioning=pos), "You are an elite career consultant.", temperature=0.7)

    async def generate_form_answers(self, profile: Dict[str, Any], job: Dict[str, Any], questions: List[str]) -> List[Dict[str, str]]:
        res = await self._call_json(FORM_ANSWER_PROMPT.format(profile=json.dumps(profile), job=json.dumps(job), questions=json.dumps(questions)), "You are an expert job application assistant. Always return valid JSON.")
        if isinstance(res, dict):
            for k, v in res.items():
                if isinstance(v, list):
                    return v
        return []

    async def map_form_fields(self, profile: Dict[str, Any], elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        res = await self._call_json(MAP_FORM_PROMPT.format(profile=json.dumps(profile), elements=json.dumps(elements)), "You are a form automation expert. Always return valid JSON.")
        if isinstance(res, list):
            return res
        if isinstance(res, dict):
            for v in res.values():
                if isinstance(v, list):
                    return v
        return []

llm_client = LLMClient()
