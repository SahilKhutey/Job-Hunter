from app.agents.base_agent import BaseAgent
from app.services.content_generator import content_generator
import logging

logger = logging.getLogger(__name__)

class ApplicationAgent(BaseAgent):
    def __init__(self):
        super().__init__("application")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Generating Cover Letter and Form Answers...")
        
        profile = state.get("profile")
        job = state.get("job")
        
        if not profile or not job:
            logger.error("Missing profile or job in state.")
            return state
            
        try:
            content = content_generator.generate_application_content(profile, job)
            state["cover_letter"] = content.get("cover_letter")
            state["form_answers"] = content.get("answers")
            state["positioning"] = content.get("positioning")
            logger.info(f"[Agent: {self.name}] Application content generated successfully.")
        except Exception as e:
            logger.error(f"Error generating application content: {e}")
            
        return state
