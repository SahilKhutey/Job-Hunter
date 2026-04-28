from app.agents.base_agent import BaseAgent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LearningAgent(BaseAgent):
    def __init__(self):
        super().__init__("learning")

    async def run(self, state: Dict[str, Any], db: AsyncSession = None) -> Dict[str, Any]:
        """
        Analyzes user behavior/feedback and adjusts matching weights (Async).
        """
        logger.info(f"[Agent: {self.name}] Analyzing feedback loop...")
        
        feedback = state.get("feedback")
        profile_id = state.get("profile_id")
        
        if not feedback or not profile_id or not db:
            return state
            
        # Example Logic: If user gets an interview, reinforce the current matching parameters
        # If user rejects a match, decrease weights for the mismatched attributes
        
        stmt = select(Profile).filter(Profile.id == profile_id)
        result = await db.execute(stmt)
        profile = result.scalar_one_or_none()
        
        if not profile:
            return state
            
        weights = profile.preference_weights or {
            "skills": 1.0, 
            "experience": 1.0, 
            "education": 1.0, 
            "location": 1.0,
            "company_tier": 1.0,
            "industry_relevance": 1.0
        }
        
        if feedback == "interview_success":
            logger.info(f"[Agent: {self.name}] High-Performance event detected. Reinforcing profile DNA.")
            # Aggressive reinforcement for success
            weights["skills"] = min(weights["skills"] * 1.10, 2.0)
            weights["experience"] = min(weights["experience"] * 1.05, 2.0)
            weights["industry_relevance"] = min(weights["industry_relevance"] * 1.10, 2.0)
            
        elif feedback == "match_rejected":
            reason = state.get("rejection_reason", "general")
            logger.info(f"[Agent: {self.name}] User rejected match. Reason: {reason}. Adjusting weights.")
            
            if reason in weights:
                # Decaying penalty based on frequency (simulated by fixed 0.85 for now)
                weights[reason] = max(weights[reason] * 0.85, 0.1)
            else:
                # General penalty if reason not mapped
                for k in weights: weights[k] *= 0.98
        
        elif feedback == "application_submitted":
            # Subtle reinforcement for proactive behavior
            weights["industry_relevance"] = min(weights["industry_relevance"] * 1.02, 2.0)

        profile.preference_weights = weights
        await db.commit()
        
        state["updated_weights"] = weights
        return state

    async def analyze_company_intelligence(self, company_name: str, db: AsyncSession) -> Dict[str, Any]:
        """Analyzes all jobs from a company to find recurring red flag patterns (Async)."""
        from app.models.job import Job
        from sqlalchemy import select
        from collections import Counter
        
        stmt = select(Job).filter(Job.company == company_name)
        result = await db.execute(stmt)
        jobs = result.scalars().all()
        
        if not jobs:
            return {"company": company_name, "health_score": 100, "recurring_flags": []}
            
        all_flags = []
        total_risk = 0
        for job in jobs:
            # Note: red_flags might be a string in some DB setups, assume list for now
            flags = job.red_flags or []
            all_flags.extend(flags)
            total_risk += job.strategic_risk_score or 0
            
        avg_risk = total_risk / len(jobs)
        health_score = max(0, 100 - avg_risk)
        
        counts = Counter(all_flags)
        recurring = [f for f, c in counts.items() if (c / len(jobs)) >= 0.5] 
        
        return {
            "company": company_name,
            "health_score": round(health_score, 1),
            "recurring_flags": recurring,
            "sample_size": len(jobs),
            "intelligence_level": "HI_FIDELITY" if len(jobs) > 3 else "LOW_CONFIDENCE"
        }
