# In order to avoid circular imports, we import the task dynamically or inside the function
import logging

logger = logging.getLogger(__name__)

def enqueue_applications(user_id: int, jobs: list):
    """Batches jobs into the Celery execution queue."""
    from app.workers.tasks import apply_job_task
    
    logger.info(f"Enqueuing {len(jobs)} applications for user {user_id}")
    for job in jobs:
        # job should be a dict containing job info
        apply_job_task.delay(user_id, job)
