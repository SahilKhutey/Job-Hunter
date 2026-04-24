from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__("profile")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Structuring User Profile...")
        
        profile = state.get("profile", {})
        
        # Example enrichment or standardization logic could go here
        # E.g., inferring a general summary if one doesn't exist
        if not profile.get("summary") and profile.get("skills"):
            profile["summary"] = f"Experienced professional skilled in {', '.join(profile.get('skills', [])[:3])}"
            
        state["profile"] = profile
        logger.info(f"[Agent: {self.name}] Profile structured.")
        return state
