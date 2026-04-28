from app.agents.base_agent import BaseAgent
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ProfileAgent(BaseAgent):
    def __init__(self):
        super().__init__("profile")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Async run for ProfileAgent."""
        logger.info(f"[Agent: {self.name}] Structuring User Profile...")
        
        profile = state.get("profile", {})
        
        if not profile.get("summary") and profile.get("skills"):
            profile["summary"] = f"Experienced professional skilled in {', '.join(profile.get('skills', [])[:3])}"
            
        state["profile"] = profile
        logger.info(f"[Agent: {self.name}] Profile structured.")
        return state
