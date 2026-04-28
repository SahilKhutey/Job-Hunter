import asyncio
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from app.services.application_engine import application_engine
from app.agents.discovery_agent import DiscoveryAgent
from app.core.database import get_db
from app.models.profile import Profile

router = APIRouter()
logger = logging.getLogger(__name__)

class ApplicationRequest(BaseModel):
    job_id: str
    job_url: str
    profile_id: int
    resume_path: Optional[str] = None
    job_risk_score: Optional[float] = 0.0
    job_red_flags: Optional[list] = []

@router.post("/apply")
async def start_apply(req: ApplicationRequest, db: Session = Depends(get_db)):
    """Triggers the background application process for a specific job."""
    profile = db.query(Profile).filter(Profile.id == req.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Correctly access job_title and other data from structured_data if not at top level
    structured = profile.structured_data or {}
    user_identity = {
        "id": profile.id,
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "job_title": structured.get("job_title", ""),
        "skills": profile.skills or [],
        "structured_data": structured,
        "job_risk_score": req.job_risk_score,
        "job_red_flags": req.job_red_flags
    }
    
    # Logic to find the latest tailored resume if not provided
    resume_path = req.resume_path
    if not resume_path or resume_path == "default_resume.pdf":
        import os
        resume_dir = "static/resumes"
        if os.path.exists(resume_dir):
            # Find files like tailored_resume_{user_id}_...
            files = [os.path.join(resume_dir, f) for f in os.listdir(resume_dir) if f.startswith(f"tailored_resume_{profile.id}")]
            if files:
                resume_path = max(files, key=os.path.getmtime)
    
    # Start the background application task
    await application_engine.start_application(
        req.job_id,
        req.job_url,
        user_identity,
        resume_path
    )
    
    return {"status": "started", "job_id": req.job_id}
    
@router.post("/confirm/{job_id}")
async def confirm_application(job_id: str):
    """Resumes a paused application process."""
    from app.services.automation_service import automation_service
    success = await automation_service.confirm_application(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="No pending application found for this job ID")
    return {"status": "confirmed", "job_id": job_id}

@router.get("/status/{job_id}")
async def get_apply_status(job_id: str):
    """Returns the current status of an ongoing application."""
    status = application_engine.get_status(job_id)
    return {"status": status}

@router.post("/discover")
async def discover_jobs(
    query: str,
    location: str = "Remote",
    user_id: str = "0",
    db: Session = Depends(get_db)
):
    """Triggers the DiscoveryAgent to find new jobs in the background."""
    agent = DiscoveryAgent(user_id, db)
    # Run in background to not block the request
    asyncio.create_task(agent.run({"search_query": query, "search_location": location}))
    return {"status": "Discovery started", "query": query}
