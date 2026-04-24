import logging
from app.core.database import SessionLocal
from app.models.job import Job

logger = logging.getLogger(__name__)

def log_application(user_id: int, job_id: int, status: str):
    """Tracks application status in the database."""
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            # You would ideally have an Application table to link user_id and job_id
            # For MVP, we might just log it or update the job's AI decision state to APPLIED
            logger.info(f"User {user_id} -> Job {job_id}: {status}")
            
            if status == "submitted":
                job.ai_decision = "APPLIED"
            elif status == "failed":
                job.ai_decision = "FAILED"
            elif status == "awaiting_confirmation":
                job.ai_decision = "AWAITING_CONFIRMATION"
                
            db.commit()
    except Exception as e:
        logger.error(f"Error tracking application: {e}")
        db.rollback()
    finally:
        db.close()

    return {
        "user_id": user_id,
        "job_id": job_id,
        "status": status
    }
