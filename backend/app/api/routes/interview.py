from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.services.interview_service import interview_service
from app.models.job import Job
from app.models.profile import Profile
from pydantic import BaseModel
from typing import List

class StartSessionRequest(BaseModel):
    job_id: int
    profile_id: int

class ResponseRequest(BaseModel):
    question: str
    response: str

router = APIRouter()

@router.post("/start")
async def start_interview(req: StartSessionRequest, db: AsyncSession = Depends(get_db)):
    job_stmt = select(Job).filter(Job.id == req.job_id)
    job_result = await db.execute(job_stmt)
    job = job_result.scalar_one_or_none()
    
    profile_stmt = select(Profile).filter(Profile.id == req.profile_id)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalar_one_or_none()
    
    if not job or not profile:
        raise HTTPException(status_code=404, detail="Job or Profile not found")
        
    # Convert models to dict for the service
    job_dict = {"title": job.title, "company": job.company, "description": job.description}
    profile_dict = {"summary": profile.summary}
    
    questions = await interview_service.generate_questions(job_dict, profile_dict)
    return {"session_id": "sim_" + str(req.job_id), "questions": questions}

@router.post("/respond")
async def evaluate_answer(req: ResponseRequest):
    feedback = await interview_service.evaluate_response(req.question, req.response)
    return feedback
