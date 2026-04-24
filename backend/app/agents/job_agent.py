from app.agents.base_agent import BaseAgent
from app.ai.llm_client import llm_client
import logging

logger = logging.getLogger(__name__)

class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("job")

    def run(self, state: dict) -> dict:
        logger.info(f"[Agent: {self.name}] Analyzing Job Description...")
        
        job = state.get("job", {})
        if not job.get("description"):
            logger.warning("No job description found in state.")
            return state

        # If it's already analyzed, skip
        if not job.get("skills_required"):
            analysis = llm_client.analyze_job(job["description"])
            
            # Merge the analysis back into the job dictionary
            for k, v in analysis.items():
                job[k] = v
                
        state["job"] = job
        logger.info(f"[Agent: {self.name}] Job analysis complete.")
        return state
