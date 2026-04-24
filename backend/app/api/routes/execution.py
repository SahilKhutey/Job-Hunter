from fastapi import APIRouter, Depends, HTTPException
from app.services.application_engine import application_engine
from app.services.automation_service import automation_service
from app.core.database import get_db
from app.models.profile import Profile
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter()

@router.post("/apply/{job_id}")
async def apply_to_job(job_id: str, job_url: str, platform: str, profile_id: int, db: Session = Depends(get_db)):
    """Starts an automated application for a specific job."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    # Prepare user profile data for automation
    user_profile = {
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "skills": profile.skills,
        "structured_data": profile.structured_data
    }
    
    await application_engine.start_application(job_id, job_url, platform, user_profile)
    return {"status": "started", "job_id": job_id}

@router.post("/confirm/{job_id}")
async def confirm_application(job_id: str):
    """Confirm a paused application submission."""
    success = await automation_service.confirm_application(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="No pending confirmation found for this job.")
    return {"status": "confirmed", "job_id": job_id}

@router.get("/status/{job_id}")
def get_application_status(job_id: str):
    return {"job_id": job_id, "status": application_engine.get_status(job_id)}
