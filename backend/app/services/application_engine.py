import logging
import asyncio
from typing import Dict, Any
from app.agents.application_agent import ApplicationAgent
from app.agents.job_agent import JobAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.resume_agent import ResumeAgent
from app.agents.orchestrator import Orchestrator
from app.core.database import SessionLocal
from app.models.job import Job


logger = logging.getLogger(__name__)

class ApplicationEngine:
    """
    Service layer to manage multiple application tasks.
    """
    def __init__(self):
        self.active_tasks: Dict[str, str] = {} # job_id -> status

    async def start_application(self, job_id: str, job_url: str, profile_data: Dict[str, Any], resume_path: str):
        """
        Launches an autonomous application agent for a specific job.
        """
        self.active_tasks[job_id] = "Starting..."
        
        # Fire and forget or run in a background task
        asyncio.create_task(self._run_agent(job_id, job_url, profile_data, resume_path))
        
        return {"job_id": job_id, "status": "Initiated"}

    async def _run_agent(self, job_id: str, job_url: str, profile_data: Dict[str, Any], resume_path: str):
        db = SessionLocal()
        try:
            self.active_tasks[job_id] = "Initializing Pipeline..."
            user_id = str(profile_data.get("id", "default"))
            
            # Phase 3: Define Parallel Stages
            # Stage 1: Analyze the Job (sequential because others depend on it)
            # Stage 2: Match and Tailor Resume in Parallel
            # Stage 3: Autonomous Application
            
            stages = [
                [JobAgent()],
                [MatchingAgent(), ResumeAgent()],
                [ApplicationAgent(user_id, profile_data, db)]
            ]
            
            orchestrator = Orchestrator(stages)
            
            initial_state = {
                "job": {"id": int(job_id), "url": job_url, "description": ""}, # Description will be filled by JobAgent
                "profile": profile_data,
                "resume_path": resume_path
            }
            
            self.active_tasks[job_id] = "Executing Stages..."
            final_state = await orchestrator.run(initial_state)
            
            if final_state.get("error"):
                self.active_tasks[job_id] = f"Error: {final_state['error']}"
            else:
                # Update Job record with latest scores
                job_record = db.query(Job).filter(Job.id == int(job_id)).first()
                if job_record:
                    job_record.match_score = final_state.get("match_score", 0.0)
                    job_record.match_analytics = final_state.get("match_analytics", {})
                    db.commit()
                
                self.active_tasks[job_id] = "Completed"
                
        except Exception as e:
            logger.error(f"Engine error for job {job_id}: {e}")
            self.active_tasks[job_id] = f"Error: {str(e)}"
        finally:
            db.close()


    def get_status(self, job_id: str):
        return self.active_tasks.get(job_id, "Not Found")

application_engine = ApplicationEngine()
