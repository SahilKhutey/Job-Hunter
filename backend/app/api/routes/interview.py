from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.interview_service import interview_service
from app.models.job import Job
from app.models.profile import Profile
from pydantic import BaseModel
from typing import List

router = APIRouter()

class StartSessionRequest(BaseModel):
    job_id: int
    profile_id: int

class ResponseRequest(BaseModel):
    question: str
    response: str

@router.post("/start")
async def start_interview(req: StartSessionRequest, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == req.job_id).first()
    profile = db.query(Profile).filter(Profile.id == req.profile_id).first()
    
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
