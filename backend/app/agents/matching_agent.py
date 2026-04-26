from app.agents.base_agent import BaseAgent
from app.services.resume_tailor import resume_tailor
import logging

logger = logging.getLogger(__name__)

class MatchingAgent(BaseAgent):
    def __init__(self):
        super().__init__("matching")

    async def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Calculating Match Score...")
        
        profile = state.get("profile", {})
        job = state.get("job", {})
        
        user_skills = profile.get("skills", [])
        job_skills = job.get("skills_required", [])
        
        if not user_skills or not job_skills:
            state["match_score"] = 0.5
            return state

        # We can reuse the gap/alignment logic from resume_tailor
        matched, missing = resume_tailor.analyze_alignment(user_skills, job_skills)
        
        match_ratio = len(matched) / len(job_skills) if job_skills else 0.5
        # Base semantic score (mocked here, but would be fetched via FAISS usually)
        base_score = 0.6 
        score = base_score + (match_ratio * 0.4) # Max 1.0
            
        state["match_score"] = score
        state["match_analytics"] = {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "alignment_ratio": match_ratio,
            "recommendation": "Strong Match" if score > 0.8 else "Needs Tailoring"
        }
        logger.info(f"[Agent: {self.name}] Match score: {score}. Matched: {len(matched)}, Missing: {len(missing)}")
        
        return state
