from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User, UserIdentity
from app.services.resume_parser import extract_resume_text
from app.services.resume_ai import parse_resume_to_json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])
logger = logging.getLogger(__name__)

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Uploads a resume, extracts text, structures it via AI (Async), and returns the suggested profile.
    """
    try:
        content = await file.read()
        text = extract_resume_text(file.filename, content)
        
        # Structuring via AI (Awaited)
        structured_data = await parse_resume_to_json(text)
        
        return {
            "status": "success",
            "profile": structured_data
        }
    except Exception as e:
        logger.error(f"Onboarding Upload Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

from app.models.profile import Profile

@router.post("/confirm")
async def confirm_onboarding(
    profile_data: dict, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    """
    Finalizes onboarding by saving the reviewed and edited profile data.
    """
    stmt = select(UserIdentity).filter(UserIdentity.user_id == current_user.id)
    result = await db.execute(stmt)
    identity = result.scalar_one_or_none()
    
    if not identity:
        identity = UserIdentity(user_id=current_user.id)
        db.add(identity)

    # Ensure a Profile object also exists
    p_stmt = select(Profile).filter(Profile.user_id == current_user.id)
    p_result = await db.execute(p_stmt)
    profile = p_result.scalar_one_or_none()
    
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    # Map the structured profile data to the UserIdentity model
    identity.full_name = profile_data.get("full_name", identity.full_name)
    identity.phone = profile_data.get("phone", identity.phone)
    identity.location = profile_data.get("location", identity.location)
    
    # Store complex structures in answers field
    identity.answers = {
        "summary": profile_data.get("summary"),
        "experience": profile_data.get("experience"),
        "education": profile_data.get("education"),
        "job_title": profile_data.get("job_title"),
        "skills": profile_data.get("skills", [])
    }
    
    links = profile_data.get("links", {})
    identity.linkedin_url = links.get("linkedin", identity.linkedin_url)
    identity.github_url = links.get("github", identity.github_url)
    identity.portfolio_url = links.get("portfolio", identity.portfolio_url)

    await db.commit()
    return {"status": "success", "message": "Onboarding complete"}
