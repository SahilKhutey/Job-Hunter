from app.agents.base_agent import BaseAgent
from app.services.resume_tailor import resume_tailor
import logging

logger = logging.getLogger(__name__)

class ResumeAgent(BaseAgent):
    def __init__(self):
        super().__init__("resume")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Tailoring Resume...")
        
        profile = state.get("profile")
        job = state.get("job")
        
        if not profile or not job:
            logger.error("Missing profile or job in state.")
            return state

        try:
            result = resume_tailor.generate_tailored_resume(profile, job)
            state["resume_json"] = result.get("resume_json")
            state["resume_pdf_path"] = result.get("pdf_path")
            logger.info(f"[Agent: {self.name}] Resume tailored and PDF generated.")
        except Exception as e:
            logger.error(f"Error generating tailored resume: {e}")
            
        return state
