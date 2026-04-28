from app.ai.llm_client import llm_client
from typing import List, Dict, Any

INTERVIEW_PROMPT = """
You are an expert interviewer for a {role} position at {company}.

CONTEXT:
Candidate Profile: {profile_summary}
Job Description: {job_description}
STRATEGIC RISK SIGNALS: {risk_context}

TASK:
Generate {count} high-stakes interview questions.

REQUIREMENTS:
1. TECHNICAL DEPTH: 40% of questions must test core engineering/domain architecture.
2. STRATEGIC SURVIVAL: If Risk Signals are present, include 1 question that helps the candidate "reverse interview" the company (e.g., asking about the red flags tactfully).
3. BEHAVIORAL PRESSURE: Use Socratic questioning to test resilience and decision-making.
4. VARIETY: Mix of Technical, Behavioral, and Strategic questions.

Return as JSON list: [{{ "id": 1, "question": "...", "type": "technical|behavioral|strategic", "intent": "What this question really tests" }}].
"""

FEEDBACK_PROMPT = """
As an elite technical recruiter, evaluate the candidate's response to: "{question}"
Candidate Response: "{response}"

Provide a multi-dimensional assessment:
1. Score (0-100)
2. Confidence & Tone Assessment (Analyze the linguistic confidence)
3. Technical Accuracy (Check for specific keywords and concepts)
4. Coaching (Actionable advice for improvement)
5. Model Answer (How a top 1% candidate would answer)

Return as JSON: {"score": 85, "confidence": "HIGH|MED|LOW", "accuracy": 90, "feedback": "...", "suggestion": "..."}
"""

class InterviewEngine:
    async def generate_questions(self, job: Dict[str, Any], profile: Dict[str, Any], count: int = 5) -> List[Dict[str, Any]]:
        exp_level = profile.get("years_experience", 2)
        
        # Extract strategic risk context
        risk_score = job.get("strategic_risk_score", 0)
        red_flags = job.get("red_flags", [])
        risk_context = "No major risks detected."
        if risk_score > 60 or red_flags:
            risk_context = f"High Risk (Score: {risk_score}). Red Flags: {', '.join(red_flags)}"

        prompt = INTERVIEW_PROMPT.format(
            role=job.get("title", "Software Engineer"),
            company=job.get("company", "Tech Co"),
            profile_summary=f"Candidate with {exp_level} years of experience. Summary: {profile.get('summary', '')}",
            job_description=job.get("description", "")[:1000],
            risk_context=risk_context,
            count=count
        )
        return await llm_client.generate_structured_json(prompt)

    async def evaluate_response(self, question: str, response: str) -> Dict[str, Any]:
        prompt = FEEDBACK_PROMPT.format(
            question=question,
            response=response
        )
        return await llm_client.generate_structured_json(prompt)

interview_service = InterviewEngine()
