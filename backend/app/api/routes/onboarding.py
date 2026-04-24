from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User, UserIdentity
from app.services.resume_parser import extract_resume_text
from app.services.resume_ai import parse_resume_to_json

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])
logger = logging.getLogger(__name__)

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Uploads a resume, extracts text, structures it via AI, and returns the suggested profile.
    """
    try:
        content = await file.read()
        text = extract_resume_text(file.filename, content)
        
        # Structuring via AI
        structured_data = parse_resume_to_json(text)
        
        # We don't save to DB yet; we return it for user review on the frontend.
        return {
            "status": "success",
            "profile": structured_data
        }
    except Exception as e:
        logger.error(f"Onboarding Upload Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.post("/confirm")
async def confirm_onboarding(
    profile_data: dict, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Finalizes onboarding by saving the reviewed and edited profile data.
    """
    identity = db.query(UserIdentity).filter(UserIdentity.user_id == current_user.id).first()
    if not identity:
        identity = UserIdentity(user_id=current_user.id)
        db.add(identity)

    # Map the structured profile data to the UserIdentity model
    identity.full_name = profile_data.get("full_name", identity.full_name)
    identity.phone = profile_data.get("phone", identity.phone)
    identity.location = profile_data.get("location", identity.location)
    
    # Store complex structures in JSON fields (using columns in the model if they exist)
    # The current model has phone, identity_data (json), links (json), resumes (json)
    
    identity.identity_data = {
        "summary": profile_data.get("summary"),
        "experience": profile_data.get("experience"),
        "education": profile_data.get("education"),
        "job_title": profile_data.get("job_title"),
        "skills": profile_data.get("skills", [])
    }
    
    links = profile_data.get("links", {})
    identity.links = {
        "linkedin": links.get("linkedin", ""),
        "github": links.get("github", ""),
        "portfolio": links.get("portfolio", "")
    }

    db.commit()
    return {"status": "success", "message": "Onboarding complete"}
