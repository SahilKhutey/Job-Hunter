from app.workers.celery_app import celery_app
from app.agents.run_pipeline import run_application_pipeline
from app.core.database import SessionLocal
from app.models.user import UserIdentity
from app.models.job import Job
from app.execution.engine import run_application
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="tasks.process_new_user_profile")
def task_process_new_user_profile(user_id: int):
    """Event: USER_CREATED or PROFILE_UPDATED"""
    logger.info(f"Processing new profile for user {user_id}")
    # Profile update might trigger a re-score of top jobs
    return f"Profile processed for user {user_id}"

@celery_app.task(name="tasks.score_job")
def task_score_job(user_id: int, job_id: int):
    """Event: NEW_JOB_INGESTED or MANUAL_TRIGGER"""
    logger.info(f"Scoring job {job_id} for user {user_id} via Multi-Agent Pipeline")
    db = SessionLocal()
    try:
        user = db.query(UserIdentity).filter(UserIdentity.id == user_id).first()
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not user or not job:
            return "User or Job not found."
            
        profile_dict = {
            "id": user.id,
            "full_name": user.full_name,
            "skills": user.answers.get("skills", []) if user.answers else [],
            "experience": user.answers.get("experience", []) if user.answers else []
        }
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "url": job.url
        }

        # Run the Multi-Agent Pipeline
        final_state = run_application_pipeline(profile_dict, job_dict)
        
        # Update Job decision
        if "action_decision" in final_state:
            job.ai_decision = final_state["action_decision"]
            job.match_score = final_state.get("match_score", 0.0)
            db.commit()
            
        return f"Pipeline completed for job {job_id} with decision {job.ai_decision}"
    except Exception as e:
        logger.error(f"Task failed: {e}")
        db.rollback()
    finally:
        db.close()

@celery_app.task(bind=True, name="tasks.apply_job_task", max_retries=3)
def apply_job_task(self, user_id: int, job_dict: dict):
    """Celery task to handle async execution engine flow with retries."""
    logger.info(f"Starting execution task for user {user_id}, job {job_dict.get('id')}")
    
    # We need the profile for execution
    db = SessionLocal()
    try:
        user = db.query(UserIdentity).filter(UserIdentity.id == user_id).first()
        if not user:
            logger.error("User not found for execution task.")
            return "Failed: User not found."
            
        profile_dict = {
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.answers.get("phone", "") if user.answers else "",
            "linkedin": user.answers.get("linkedin", "") if user.answers else "",
            "github": user.answers.get("github", "") if user.answers else ""
        }
        
        # We pass profile in directly since it shouldn't query db inside the engine to stay decoupled
        return run_application(user_id, job_dict, profile_dict)
        
    except Exception as e:
        logger.error(f"Application execution failed: {e}. Retrying...")
        # Countdown sets a backoff delay for the retry
        self.retry(exc=e, countdown=30)
    finally:
        db.close()
