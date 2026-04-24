from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job
from app.models.user import UserIdentity
from app.services.resume_tailor import resume_tailor
from app.services.content_generator import content_generator
from typing import Optional

router = APIRouter()

@router.post("/generate-tailored-resume")
def generate_tailored_resume(job_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """
    Triggers the AI Resume Tailoring Engine.
    Generates an ATS-optimized JSON resume and a PDF.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    user = db.query(UserIdentity).filter(UserIdentity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Identity not found")

    # Serialize objects for the engine
    profile_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "skills": user.answers.get("skills", []) if user.answers else [],
        "experience": user.answers.get("experience", []) if user.answers else []
    }
    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "skills_required": job.skills_required
    }

    try:
        result = resume_tailor.generate_tailored_resume(profile_dict, job_dict)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-application-content")
def generate_application_content(job_id: int, company_text: Optional[str] = None, user_id: int = 1, db: Session = Depends(get_db)):
    """
    Triggers the Cover Letter and Form Answer Generator.
    Returns highly contextualized text for application fields.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    user = db.query(UserIdentity).filter(UserIdentity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Identity not found")

    profile_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "skills": user.answers.get("skills", []) if user.answers else [],
        "experience": user.answers.get("experience", []) if user.answers else []
    }
    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description
    }

    try:
        result = content_generator.generate_application_content(profile_dict, job_dict, company_text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
