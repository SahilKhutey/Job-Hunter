from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.profile import Profile
from app.models.job import Job
from app.agents.run_pipeline import run_application_pipeline

router = APIRouter()

@router.post("/run-pipeline")
def trigger_agent_pipeline(user_id: int, job_id: int, db: Session = Depends(get_db)):
    """
    Triggers the Multi-Agent Orchestration Pipeline for a specific user and job.
    """
    user = db.query(Profile).filter(Profile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    profile_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "skills": user.skills or [],
        "experience": (user.structured_data or {}).get("experience", [])
    }
    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "url": job.url
    }

    try:
        # In a real async environment, this would be pushed to Celery.
        # For the API response, we run it synchronously here to return the state.
        final_state = run_application_pipeline(profile_dict, job_dict)
        
        # Update Job DB based on execution agent's decision
        if "action_decision" in final_state:
            job.ai_decision = final_state["action_decision"]
            job.match_score = final_state.get("match_score", 0.0)
            db.commit()
            
        return {"status": "success", "state": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AgentCommand(BaseModel):
    command: str
    profile_id: Optional[int] = None

@router.post("/command")
async def process_agent_command(
    cmd: AgentCommand, 
    db: Session = Depends(get_db)
):
    """
    Processes a natural language command from the Assistant UI.
    """
    # For now, return a generic acknowledgment or trigger a specific logic
    text = cmd.command.lower()
    
    if "apply" in text:
        return {"response": "I've started the application sequence for you. I'll prioritize jobs that match your profile. Check the Live Automation tab for updates."}
    
    if "match" in text or "score" in text:
        return {"response": "I'm re-running the match engine now. Your job feed will be updated with fresh scores momentarily."}
    
    if "resume" in text:
        return {"response": "Opening Profile Studio. I can help you tailor specific sections or regenerate your summary based on your experience."}
        
    return {"response": "Got it. I'm on it. I'll coordinate with the other agents to get that handled."}

