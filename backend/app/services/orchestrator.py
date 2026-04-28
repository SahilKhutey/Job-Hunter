from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import UserIdentity
from app.models.job import Job
from app.services.matching_service import matching_engine
import logging

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        pass

    async def run_pipeline(self, user_id: int = 1):
        """
        Master Pipeline (Async):
        1. Get User Profile
        2. Get Unscored Jobs
        3. Match & Rank
        4. Make AI Decision
        """
        from app.api.routes.websocket import emit_agent_update
        
        # Mission State
        mission = {
            "user_id": user_id,
            "status": "initializing",
            "jobs_processed": 0,
            "errors": []
        }
        
        await emit_agent_update("Coordinator", "running", "Initializing Hunter AI Mission Control...", user_id=user_id)
        
        async with AsyncSessionLocal() as db:
            try:
                # 1. Get Profile
                stmt_profile = select(UserIdentity).filter(UserIdentity.id == user_id)
                result_profile = await db.execute(stmt_profile)
                profile = result_profile.scalar_one_or_none()
                
                if not profile:
                    await emit_agent_update("Coordinator", "error", f"No profile found for user {user_id}.", user_id=user_id)
                    return
 
                # 2. Fetch Jobs
                await emit_agent_update("Discovery", "running", "Scanning for PENDING jobs...", user_id=user_id)
                stmt_jobs = select(Job).filter(Job.ai_decision == "PENDING")
                result_jobs = await db.execute(stmt_jobs)
                jobs = result_jobs.scalars().all()
                
                if not jobs:
                    await emit_agent_update("Discovery", "success", "Mission Complete: No new jobs to process.", user_id=user_id)
                    return
 
                # 3. Match and Rank (Recovery Logic)
                await emit_agent_update("Intelligence", "running", f"Analyzing compatibility for {len(jobs)} jobs...", user_id=user_id)
                try:
                    matches = await matching_engine.match_jobs(profile, jobs)
                except Exception as me:
                    logger.error(f"Matching Engine Failure: {me}")
                    await emit_agent_update("Intelligence", "error", "Critical failure in Matching Engine. Retrying with heuristics...", user_id=user_id)
                    # Fallback to simple matching if semantic fails
                    matches = [(j, 0.5) for j in jobs]
 
                for job, score in matches:
                    job.match_score = score
                    
                    # AI Decision Layer
                    if score >= 0.85:
                        job.ai_decision = "AUTO_APPLY_READY"
                    elif score >= 0.65:
                        job.ai_decision = "REVIEW"
                    else:
                        job.ai_decision = "IGNORE"
                    
                    db.add(job)
                    mission["jobs_processed"] += 1
 
                await db.commit()
                await emit_agent_update("Coordinator", "success", f"Pipeline completed. {len(jobs)} jobs ranked.", user_id=user_id)
                
            except Exception as e:
                logger.error(f"Mission Critical Failure: {e}")
                await db.rollback()
                await emit_agent_update("Coordinator", "error", f"Mission aborted: {str(e)}", user_id=user_id)

    async def process_feedback(self, profile_id: int, feedback_type: str, reason: str = None):
        """
        Process user feedback to refine the matching model (Async).
        """
        from app.agents.learning_agent import LearningAgent
        agent = LearningAgent()
        
        async with AsyncSessionLocal() as db:
            state = {
                "profile_id": profile_id,
                "feedback": feedback_type,
                "rejection_reason": reason
            }
            await agent.run(state, db=db)

orchestrator = Orchestrator()
