from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import os

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User, UserIdentity
from app.services.resume_tailor import tailor_resume
from app.services.resume_pdf import generate_resume_pdf
from app.services.resume_scorer import score_resume
from app.services.resume_fix_pipeline import auto_fix_resume_pipeline



router = APIRouter(prefix="/resume", tags=["Resume Optimization"])
logger = logging.getLogger(__name__)

@router.post("/tailor")
async def tailor_resume_endpoint(
    payload: dict, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Takes a job description and the user's base profile, returns a tailored JSON resume and a PDF download path.
    """
    try:
        job_description = payload.get("job_description")
        if not job_description:
            raise HTTPException(status_code=400, detail="Job description is required")

        # Get user's base profile from identity_data
        identity = db.query(UserIdentity).filter(UserIdentity.user_id == current_user.id).first()
        if not identity or not identity.identity_data:
            raise HTTPException(status_code=404, detail="User profile not found. Please complete onboarding first.")

        base_profile = identity.identity_data
        
        # Add basic info from identity if not in identity_data
        base_profile["full_name"] = identity.full_name
        base_profile["email"] = current_user.email
        base_profile["phone"] = identity.phone
        base_profile["location"] = identity.location

        # AI Tailoring
        tailored_data = tailor_resume(base_profile, job_description)
        
        # Generate PDF
        # We'll store it in a public-accessible dir or a temporary one
        # For this prototype, we'll use an 'outputs' folder
        filename = f"tailored_resume_{current_user.id}_{int(os.times()[4])}.pdf"
        output_dir = "static/resumes"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        generate_resume_pdf(tailored_data, file_path)

        return {
            "status": "success",
            "resume": tailored_data,
            "pdf_url": f"/static/resumes/{filename}"
        }
    except Exception as e:
        logger.error(f"Tailoring Route Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score")
async def score_resume_endpoint(
    payload: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Evaluates a resume against a job description.
    Expects resume_text, resume_json, and job_description in payload.
    """
    try:
        resume_text = payload.get("resume_text")
        resume_json = payload.get("resume_json")
        job_description = payload.get("job_description")

        if not resume_text or not job_description:
            raise HTTPException(status_code=400, detail="Missing required evaluation data")

        results = score_resume(resume_text, resume_json or {}, job_description)
        return results
    except Exception as e:
        logger.error(f"Scoring Route Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fix")
async def fix_resume_endpoint(
    payload: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Automatically improves a resume based on a job description.
    """
    try:
        resume_text = payload.get("resume_text")
        resume_json = payload.get("resume_json")
        job_description = payload.get("job_description")

        if not resume_text or not job_description:
            raise HTTPException(status_code=400, detail="Missing required optimization data")

        results = auto_fix_resume_pipeline(resume_text, resume_json or {}, job_description)
        return results
    except Exception as e:
        logger.error(f"Fix Route Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


