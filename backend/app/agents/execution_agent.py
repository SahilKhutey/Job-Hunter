from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ExecutionAgent(BaseAgent):
    def __init__(self):
        super().__init__("execution")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Preparing execution strategy...")
        
        # In a real environment, this might trigger the Playwright script
        # OR it might just queue it for UI confirmation as per "Safe Mode".
        
        job = state.get("job", {})
        score = state.get("match_score", 0.0)
        
        if score >= 0.85:
            state["action_decision"] = "AUTO_APPLY_READY"
            logger.info(f"[Agent: {self.name}] Job queued for Auto-Apply Confirmation.")
        elif score >= 0.65:
            state["action_decision"] = "REVIEW"
            logger.info(f"[Agent: {self.name}] Job queued for Manual Review.")
        else:
            state["action_decision"] = "IGNORE"
            logger.info(f"[Agent: {self.name}] Job Ignored.")
            
        return state
