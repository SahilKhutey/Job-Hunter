from app.workers.celery_app import celery_app
from app.agents.run_pipeline import run_application_pipeline
from app.core.database import SessionLocal
from app.models.user import UserIdentity, User
from app.models.job import Job
from app.execution.engine import run_application
import logging
import asyncio

logger = logging.getLogger(__name__)

@celery_app.task(name="tasks.process_new_user_profile")
def task_process_new_user_profile(user_id: int):
    """Event: USER_CREATED or PROFILE_UPDATED"""
    logger.info(f"Processing new profile for user {user_id}")
    return f"Profile processed for user {user_id}"

from sqlalchemy import select
from app.core.database import AsyncSessionLocal

async def _score_job_logic(user_id: int, job_id: int):
    async with AsyncSessionLocal() as db:
        stmt_identity = select(UserIdentity).filter(UserIdentity.id == user_id)
        result_identity = await db.execute(stmt_identity)
        identity = result_identity.scalar_one_or_none()
        
        stmt_job = select(Job).filter(Job.id == job_id)
        result_job = await db.execute(stmt_job)
        job = result_job.scalar_one_or_none()
        
        if not identity or not job:
            return "User or Job not found."
            
        profile_dict = {
            "id": identity.id,
            "full_name": identity.full_name,
            "skills": (identity.answers or {}).get("skills", []),
            "experience": (identity.answers or {}).get("experience", [])
        }
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "url": job.url
        }

        # Run the Multi-Agent Pipeline (Async)
        final_state = await run_application_pipeline(profile_dict, job_dict)
        
        # Update Job decision
        if "action_decision" in final_state:
            job.ai_decision = final_state["action_decision"]
            job.match_score = final_state.get("match_score", 0.0)
            await db.commit()
            
        return f"Pipeline completed for job {job_id} with decision {job.ai_decision}"

@celery_app.task(name="tasks.score_job")
def task_score_job(user_id: int, job_id: int):
    """Event: NEW_JOB_INGESTED or MANUAL_TRIGGER (Async Pipeline)"""
    logger.info(f"Scoring job {job_id} for user {user_id} via Multi-Agent Pipeline")
    try:
        return asyncio.run(_score_job_logic(user_id, job_id))
    except Exception as e:
        logger.error(f"Task score_job failed: {e}")
        return f"Error: {e}"

async def _apply_job_logic(user_id: int, job_dict: dict):
    async with AsyncSessionLocal() as db:
        stmt_identity = select(UserIdentity).filter(UserIdentity.id == user_id)
        result_identity = await db.execute(stmt_identity)
        identity = result_identity.scalar_one_or_none()
        
        if not identity:
            logger.error("User Identity not found for execution task.")
            return "Failed: Identity not found."
        
        # Fetch user for email
        stmt_user = select(User).filter(User.id == identity.user_id)
        result_user = await db.execute(stmt_user)
        user_record = result_user.scalar_one_or_none()
            
        profile_dict = {
            "full_name": identity.full_name,
            "email": user_record.email if user_record else "",
            "phone": identity.phone or "",
            "linkedin": identity.linkedin_url or "",
            "github": identity.github_url or ""
        }
        
        # Run async application engine
        return await run_application(user_id, job_dict, profile_dict)

@celery_app.task(bind=True, name="tasks.apply_job_task", max_retries=3)
def apply_job_task(self, user_id: int, job_dict: dict):
    """Celery task to handle async execution engine flow (Async)."""
    logger.info(f"Starting execution task for user {user_id}, job {job_dict.get('id')}")
    try:
        return asyncio.run(_apply_job_logic(user_id, job_dict))
    except Exception as e:
        logger.error(f"Application execution failed: {e}. Retrying...")
        self.retry(exc=e, countdown=30)
