from app.ai.llm_client import llm_client
from typing import List, Dict, Any

INTERVIEW_PROMPT = """
You are an expert interviewer for a {role} position at {company}.
Based on the candidate's profile: {profile_summary}
And the job description: {job_description}

Generate {count} high-quality interview questions that test for technical depth, culture fit, and role-specific challenges.
Return the questions as a JSON list of objects: [{"id": 1, "question": "...", "type": "technical|behavioral"}].
"""

FEEDBACK_PROMPT = """
As the interviewer, evaluate the candidate's response to the question: "{question}"
Candidate Response: "{response}"

Provide:
1. A Score (0-100)
2. Immediate Feedback (Coaching on what to improve)
3. Suggested Better Response

Return as JSON: {"score": 85, "feedback": "...", "suggestion": "..."}
"""

class InterviewEngine:
    async def generate_questions(self, job: Dict[str, Any], profile: Dict[str, Any], count: int = 5) -> List[Dict[str, Any]]:
        prompt = INTERVIEW_PROMPT.format(
            role=job.get("title", "Software Engineer"),
            company=job.get("company", "Tech Co"),
            profile_summary=profile.get("summary", ""),
            job_description=job.get("description", "")[:1000],
            count=count
        )
        # Using LLM to generate structured questions
        return await llm_client.generate_structured_json(prompt)

    async def evaluate_response(self, question: str, response: str) -> Dict[str, Any]:
        prompt = FEEDBACK_PROMPT.format(
            question=question,
            response=response
        )
        return await llm_client.generate_structured_json(prompt)

interview_service = InterviewEngine()
