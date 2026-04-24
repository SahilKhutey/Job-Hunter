from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class LearningAgent(BaseAgent):
    def __init__(self):
        super().__init__("learning")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Analyzing feedback loop...")
        
        feedback = state.get("feedback")
        
        if feedback == "interview":
            state["score_boost"] = True
            logger.info(f"[Agent: {self.name}] Positive feedback registered. Adjusting weights.")
            # In a full implementation, we'd update vector weights or user preferences in DB
            
        return state
