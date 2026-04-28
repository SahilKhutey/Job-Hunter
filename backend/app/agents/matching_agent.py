from app.agents.base_agent import BaseAgent
from app.services.matching_service import matching_service
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MatchingAgent(BaseAgent):
    def __init__(self):
        super().__init__("matching")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Async run for MatchingAgent using the refined MatchingEngine."""
        logger.info(f"[Agent: {self.name}] Calculating Match Score...")
        
        profile = state.get("profile", {})
        job = state.get("job", {})
        
        if not profile or not job:
            logger.warning("Missing profile or job for matching.")
            state["match_score"] = 0.0
            return state

        # Use the unified matching service
        metrics = await matching_service.calculate_metrics(profile, job)
        
        state["match_score"] = metrics["match_score"]
        state["match_analytics"] = {
            "matched_skills": metrics.get("matched_skills", []),
            "missing_skills": metrics.get("skill_gap", []),
            "difficulty": metrics.get("difficulty", 0.5),
            "priority": metrics.get("priority", "MEDIUM"),
            "recommendation": "Strong Match" if metrics["match_score"] > 0.8 else "Needs Tailoring"
        }
        
        logger.info(f"[Agent: {self.name}] Match score: {state['match_score']}. Matched: {len(state['match_analytics']['matched_skills'])}")
        
        return state
