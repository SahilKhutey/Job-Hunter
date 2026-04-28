import logging
import asyncio
from typing import Dict, Any
from app.agents.application_agent import ApplicationAgent
from app.agents.job_agent import JobAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.resume_agent import ResumeAgent
from app.agents.orchestrator import Orchestrator
from app.agents.pipeline import pipeline
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.job import Job

logger = logging.getLogger(__name__)

class ApplicationEngine:
    """
    Service layer to manage multiple application tasks (Async).
    """
    def __init__(self):
        self.active_tasks: Dict[str, str] = {} # job_id -> status

    async def start_application(self, job_id: str, job_url: str, profile_data: Dict[str, Any], resume_path: str):
        """
        Launches an autonomous application agent for a specific job (Async).
        """
        self.active_tasks[job_id] = "Starting..."
        
        # Fire and forget or run in a background task
        asyncio.create_task(self._run_agent(job_id, job_url, profile_data, resume_path))
        
        return {"job_id": job_id, "status": "Initiated"}

    async def _run_agent(self, job_id: str, job_url: str, profile_data: Dict[str, Any], resume_path: str):
        async with AsyncSessionLocal() as db:
            try:
                self.active_tasks[job_id] = "Initializing Pipeline..."
                user_id = str(profile_data.get("id", "default"))
                
                # Fetch job from DB to get existing description or other metadata
                stmt = select(Job).filter(Job.id == int(job_id))
                result = await db.execute(stmt)
                job_record = result.scalar_one_or_none()
                
                job_data = {
                    "id": int(job_id), 
                    "url": job_url, 
                    "description": job_record.description if job_record else "",
                    "title": job_record.title if job_record else "",
                    "company": job_record.company if job_record else ""
                }
                
                # Define Pipeline Stages
                stages = [
                    [JobAgent()], # Stage 1: Analyze Job (fills description/skills if missing)
                    [MatchingAgent(), ResumeAgent()], # Stage 2: Parallel Match & Tailor
                    [ApplicationAgent(user_id, profile_data, db)] # Stage 3: Deploy
                ]
                
                orchestrator = Orchestrator(stages)
                
                initial_state = {
                    "job": job_data,
                    "profile": profile_data,
                    "resume_pdf_path": resume_path,
                    "action_decision": "AUTO_APPLY_READY" # Default to ready if we are in this engine
                }
                
                self.active_tasks[job_id] = "Executing Stages..."
                final_state = await orchestrator.run(initial_state)
                
                if final_state.get("error"):
                    self.active_tasks[job_id] = f"Error: {final_state['error']}"
                else:
                    # Update Job record with latest scores and status
                    if job_record:
                        job_record.match_score = final_state.get("match_score", job_record.match_score)
                        job_record.match_analytics = final_state.get("match_analytics", job_record.match_analytics)
                        await db.commit()
                    
                    self.active_tasks[job_id] = "Completed"
                    
            except Exception as e:
                logger.error(f"Engine error for job {job_id}: {e}")
                self.active_tasks[job_id] = f"Error: {str(e)}"

    def get_status(self, job_id: str):
        return self.active_tasks.get(job_id, "Not Found")

application_engine = ApplicationEngine()
