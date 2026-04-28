from app.agents.base_agent import BaseAgent
from app.ai.llm_client import llm_client
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class JobAgent(BaseAgent):
    def __init__(self):
        super().__init__("job")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Async run for JobAgent with awaited LLM call."""
        logger.info(f"[Agent: {self.name}] Analyzing Job Description...")
        
        job = state.get("job", {})
        if not job.get("description"):
            logger.warning("No job description found in state.")
            return state

        # If it's already analyzed, skip
        if not job.get("skills_required"):
            # Await the async LLM call
            analysis = await llm_client.analyze_job(job["description"])
            
            for k, v in analysis.items():
                job[k] = v
                
        state["job"] = job
        logger.info(f"[Agent: {self.name}] Job analysis complete.")
        return state
