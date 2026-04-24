import logging
import asyncio
from typing import Dict, Any
from app.agents.application_agent import ApplicationAgent
from app.core.database import SessionLocal


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
            self.active_tasks[job_id] = "Initializing Browser..."
            user_id = str(profile_data.get("id", "default"))
            agent = ApplicationAgent(user_id, profile_data, db)
            
            self.active_tasks[job_id] = "Navigating to Job..."
            success = await agent.apply(int(job_id), job_url, resume_path)

            
            if success:
                self.active_tasks[job_id] = "Completed"
            else:
                self.active_tasks[job_id] = "Failed"
        except Exception as e:
            logger.error(f"Engine error for job {job_id}: {e}")
            self.active_tasks[job_id] = f"Error: {str(e)}"
        finally:
            db.close()


    def get_status(self, job_id: str):
        return self.active_tasks.get(job_id, "Not Found")

application_engine = ApplicationEngine()
