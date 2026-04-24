import asyncio
import logging
from typing import Dict, List, Optional
from app.services.automation_service import automation_service
from app.api.routes.websocket import emit_agent_update

logger = logging.getLogger(__name__)

class ApplicationEngine:
    def __init__(self):
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.history: List[Dict] = []

    async def start_application(self, job_id: str, job_url: str, platform: str, user_profile: Dict):
        """Starts an automated application task."""
        if job_id in self.active_tasks and not self.active_tasks[job_id].done():
            await emit_agent_update("System", "error", f"Application for job {job_id} is already running.")
            return

        task = asyncio.create_task(
            self._run_application(job_id, job_url, platform, user_profile)
        )
        self.active_tasks[job_id] = task
        return task

    async def _run_application(self, job_id: str, job_url: str, platform: str, user_profile: Dict):
        try:
            await automation_service.apply_to_job(job_id, job_url, platform, user_profile)
            self.history.append({
                "job_id": job_id,
                "status": "completed",
                "platform": platform
            })
        except Exception as e:
            logger.error(f"Application failed for job {job_id}: {e}")
            await emit_agent_update("Hunter AI", "error", f"Critical failure: {str(e)}")
            self.history.append({
                "job_id": job_id,
                "status": "failed",
                "error": str(e)
            })
        finally:
            if job_id in self.active_tasks:
                del self.active_tasks[job_id]

    def get_status(self, job_id: str) -> str:
        if job_id in self.active_tasks:
            return "running"
        for entry in self.history:
            if entry["job_id"] == job_id:
                return entry["status"]
        return "idle"

application_engine = ApplicationEngine()
