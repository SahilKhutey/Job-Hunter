from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.job import Job

logger = logging.getLogger(__name__)

async def log_application(user_id: int, job_id: int, status: str):
    """Tracks application status in the database (Async)."""
    async with AsyncSessionLocal() as db:
        try:
            stmt = select(Job).filter(Job.id == job_id)
            result = await db.execute(stmt)
            job = result.scalar_one_or_none()
            
            if job:
                logger.info(f"User {user_id} -> Job {job_id}: {status}")
                
                if status == "submitted":
                    job.ai_decision = "APPLIED"
                elif status == "failed":
                    job.ai_decision = "FAILED"
                elif status == "awaiting_confirmation":
                    job.ai_decision = "AWAITING_CONFIRMATION"
                    
                await db.commit()
        except Exception as e:
            logger.error(f"Error tracking application: {e}")
            await db.rollback()

    return {
        "user_id": user_id,
        "job_id": job_id,
        "status": status
    }
