from app.services.resume_tailor import resume_tailor
from app.utils.pdf_generator import pdf_generator
import logging

logger = logging.getLogger(__name__)

class ResumeAgent(BaseAgent):
    def __init__(self):
        super().__init__("resume")

    async def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Tailoring Resume...")
        
        profile = state.get("profile")
        job = state.get("job")
        
        if not profile or not job:
            logger.error("Missing profile or job in state.")
            return state

        try:
            # 1. Generate Tailored JSON
            tailored_json = resume_tailor.generate_tailored_resume(profile, job.get("description", ""))
            
            # 2. Add Contact Info back to the JSON for PDF (it's often missing in the raw tailoring prompt)
            tailored_json["full_name"] = profile.get("full_name")
            
            # 3. Generate PDF Artifact
            user_id = state.get("user_id", "0")
            job_id = job.get("id", 0)
            pdf_path = pdf_generator.generate_resume(tailored_json, user_id, job_id)
            
            state["resume_json"] = tailored_json
            state["resume_pdf_path"] = pdf_path
            
            logger.info(f"[Agent: {self.name}] Resume tailored and PDF generated at {pdf_path}")
        except Exception as e:
            logger.error(f"Error generating tailored resume: {e}")
            
        return state
