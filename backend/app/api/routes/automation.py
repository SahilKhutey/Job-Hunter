from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.application_engine import application_engine
from app.agents.discovery_agent import DiscoveryAgent
from app.core.database import get_db
from app.models.profile import Profile

router = APIRouter()

class ApplicationRequest(BaseModel):
    job_id: str
    job_url: str
    profile_id: int
    resume_path: Optional[str] = None


@router.post("/apply")
async def start_apply(req: ApplicationRequest, db: Session = Depends(get_db)):
    # Fetch real profile data
    profile = db.query(Profile).filter(Profile.id == req.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    user_identity = {
        "id": profile.id,
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "job_title": profile.job_title,
        "skills": profile.skills,
    }
    
    # Logic to find the latest tailored resume if not provided
    resume_path = req.resume_path
    if not resume_path or resume_path == "default_resume.pdf":
        import os
        resume_dir = "static/resumes"
        if os.path.exists(resume_dir):
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

@router.get("/status/{job_id}")
async def get_apply_status(job_id: str):
    status = application_engine.get_status(job_id)
    return {"status": status}
@router.post("/discover")
async def discover_jobs(
    query: str,
    location: str = "Remote",
    user_id: str = "0",
    db: Session = Depends(get_db)
):
    """Triggers the DiscoveryAgent to find new jobs."""
    agent = DiscoveryAgent(user_id, db)
    # Run in background
    asyncio.create_task(agent.run({"search_query": query, "search_location": location}))
    return {"status": "Discovery started", "query": query}
