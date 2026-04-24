from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import UserIdentity
from app.models.job import Job
from app.services.matching_service import matching_engine
import logging

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        pass

    def run_pipeline(self, user_id: int = 1):
        """
        Master Pipeline:
        1. Get User Profile
        2. Get Unscored Jobs
        3. Match & Rank
        4. Make AI Decision
        """
        db: Session = SessionLocal()
        try:
            profile = db.query(UserIdentity).filter(UserIdentity.id == user_id).first()
            if not profile:
                logger.warning(f"No profile found for user {user_id}. Aborting pipeline.")
                return

            # Fetch jobs that haven't been processed/scored yet
            jobs = db.query(Job).filter(Job.ai_decision == "PENDING").all()
            if not jobs:
                logger.info("No new jobs to process.")
                return

            # Match and Rank
            matches = matching_engine.match_jobs(profile, jobs)

            for job, score in matches:
                job.match_score = score
                
                # AI Decision Layer
                if score >= 0.85:
                    job.ai_decision = "AUTO_APPLY_READY"
                    self._queue_for_notification(job.id, user_id)
                elif score >= 0.65:
                    job.ai_decision = "REVIEW"
                else:
                    job.ai_decision = "IGNORE"
                
                db.add(job)

            db.commit()
            logger.info(f"Pipeline completed for user {user_id}. {len(jobs)} jobs processed.")
            
        except Exception as e:
            logger.error(f"Error in orchestrator pipeline: {e}")
            db.rollback()
        finally:
            db.close()

    def _queue_for_notification(self, job_id: int, user_id: int):
        """
        Since the user wants confirmation before applying, we don't trigger Playwright here.
        Instead, we might trigger a WebSocket event or update a 'Notifications' table 
        so the UI can prompt the user: 'Job X is ready for Auto-Apply. Confirm?'
        """
        logger.info(f"Job {job_id} is AUTO_APPLY_READY for user {user_id}. Waiting for user confirmation.")
        # In a real app, send a push notification or WS event here.

orchestrator = Orchestrator()
