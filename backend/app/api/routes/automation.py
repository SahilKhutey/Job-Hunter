from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.application_engine import application_engine
from app.core.database import get_db
from app.models.profile import Profile

router = APIRouter()

class ApplicationRequest(BaseModel):
    job_id: str
    job_url: str
    resume_path: str
    profile_id: int


@router.post("/apply")
async def start_apply(req: ApplicationRequest, db: Session = Depends(get_db)):
    # Fetch real profile data
    profile = db.query(Profile).filter(Profile.id == req.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    user_identity = {
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "job_title": profile.job_title,
        "skills": profile.skills,
    }
    
    # Start the background application task
    await application_engine.start_application(
        req.job_id,
        req.job_url,
        user_identity,
        req.resume_path
    )

    
    return {"status": "started", "job_id": req.job_id}

@router.get("/status/{job_id}")
async def get_apply_status(job_id: str):
    status = application_engine.get_status(job_id)
    return {"status": status}
