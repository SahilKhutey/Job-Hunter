from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.job import Job, Application
from app.models.user import UserIdentity
from app.services.resume_tailor import resume_tailor
from app.services.content_generator import content_generator
from typing import Optional

from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("/")
async def list_applications(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    """
    Lists all job applications for the current user.
    """
    stmt = select(Application).filter(Application.user_id == user_id).options(selectinload(Application.job)).order_by(Application.applied_at.desc())
    result = await db.execute(stmt)
    applications = result.scalars().all()
    
    return applications

@router.post("/generate-tailored-resume")
async def generate_tailored_resume(job_id: int, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    """
    Triggers the AI Resume Tailoring Engine.
    Generates an ATS-optimized JSON resume and a PDF.
    """
    job_stmt = select(Job).filter(Job.id == job_id)
    job_result = await db.execute(job_stmt)
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    user_stmt = select(UserIdentity).filter(UserIdentity.id == user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User Identity not found")

    # Serialize objects for the engine
    profile_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "skills": (user.answers or {}).get("skills", []),
        "experience": (user.answers or {}).get("experience", [])
    }
    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "skills_required": job.skills_required or []
    }

    try:
        # Await the async service call
        result = await resume_tailor.generate_tailored_resume(profile_dict, job_dict.get("description", ""))
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-application-content")
async def generate_application_content(job_id: int, company_text: Optional[str] = None, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    """
    Triggers the Cover Letter and Form Answer Generator.
    Returns highly contextualized text for application fields.
    """
    job_stmt = select(Job).filter(Job.id == job_id)
    job_result = await db.execute(job_stmt)
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    user_stmt = select(UserIdentity).filter(UserIdentity.id == user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User Identity not found")

    profile_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "skills": (user.answers or {}).get("skills", []),
        "experience": (user.answers or {}).get("experience", [])
    }
    job_dict = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description
    }

    try:
        # Await the async service call
        result = await content_generator.generate_application_content(profile_dict, job_dict, company_text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
