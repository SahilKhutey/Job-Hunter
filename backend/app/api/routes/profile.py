from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.services.resume_parser import extract_resume_text

from app.ai.llm_client import llm_client
from app.services.intelligence_engine import intelligence_engine
from app.models.profile import Profile
from typing import Optional
from pydantic import BaseModel

router = APIRouter()


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class ProfileCreate(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    job_title: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    target_roles: Optional[list[str]] = []
    preferred_locations: Optional[list[str]] = []
    remote_preference: Optional[str] = "Any"
    match_threshold: Optional[int] = 80

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    job_title: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    target_roles: Optional[list[str]] = None
    preferred_locations: Optional[list[str]] = None
    remote_preference: Optional[str] = None
    match_threshold: Optional[int] = None


# ── Create profile (manual, no resume required) ───────────────────────────────

@router.post("/create")
async def create_profile(data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user profile from the onboarding wizard (Async)."""
    stmt = select(Profile).filter(Profile.email == data.email)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        return {"status": "existing", "profile": _serialize(existing)}

    profile = Profile(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        location=data.location,
        skills=[],
        raw_resume_text="",
        structured_data={
            "job_title": data.job_title,
            "github_username": data.github_username,
            "linkedin_url": data.linkedin_url,
            "portfolio_url": data.portfolio_url,
            "target_roles": data.target_roles,
            "preferred_locations": data.preferred_locations,
            "remote_preference": data.remote_preference,
            "match_threshold": data.match_threshold,
        },
        links={
            "github": data.github_username,
            "linkedin": data.linkedin_url,
            "portfolio": data.portfolio_url,
        }
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return {"status": "created", "profile": _serialize(profile)}

@router.get("/{profile_id}")
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a profile by ID (Async)."""
    stmt = select(Profile).filter(Profile.id == profile_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return _serialize(profile)

@router.put("/{profile_id}")
async def update_profile(profile_id: int, data: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    """Update a profile's fields (Async)."""
    stmt = select(Profile).filter(Profile.id == profile_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if data.full_name is not None: profile.full_name = data.full_name
    if data.email is not None: profile.email = data.email
    if data.phone is not None: profile.phone = data.phone
    if data.location is not None: profile.location = data.location

    # Merge into structured_data
    sd = profile.structured_data or {}
    if data.job_title is not None: sd["job_title"] = data.job_title
    if data.github_username is not None: sd["github_username"] = data.github_username
    if data.linkedin_url is not None: sd["linkedin_url"] = data.linkedin_url
    if data.portfolio_url is not None: sd["portfolio_url"] = data.portfolio_url
    if data.target_roles is not None: sd["target_roles"] = data.target_roles
    if data.preferred_locations is not None: sd["preferred_locations"] = data.preferred_locations
    if data.remote_preference is not None: sd["remote_preference"] = data.remote_preference
    if data.match_threshold is not None: sd["match_threshold"] = data.match_threshold
    profile.structured_data = sd

    links = profile.links or {}
    if data.github_username is not None: links["github"] = data.github_username
    if data.linkedin_url is not None: links["linkedin"] = data.linkedin_url
    if data.portfolio_url is not None: links["portfolio"] = data.portfolio_url
    profile.links = links

    await db.commit()
    await db.refresh(profile)
    return {"status": "updated", "profile": _serialize(profile)}

@router.post("/{profile_id}/upload-resume")
async def upload_resume(
    profile_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a resume PDF/DOCX and extract intelligence (Async)."""
    stmt = select(Profile).filter(Profile.id == profile_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    content = await file.read()
    text = await extract_resume_text(file.filename or "resume.pdf", content)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file.")

    # Extract structured data via LLM
    extracted = await llm_client.extract_profile_data(text)

    # Merge extracted into profile
    profile.raw_resume_text = text
    if extracted.get("summary"):
        profile.summary = extracted["summary"]
    
    sd = profile.structured_data or {}
    sd.update({k: v for k, v in extracted.items() if v and k not in ("full_name", "email", "summary")})
    profile.structured_data = sd
    profile.skills = extracted.get("skills", profile.skills or [])

    # Merge top-level fields only if not already set
    if not profile.full_name and extracted.get("full_name"):
        profile.full_name = extracted["full_name"]
    if not profile.phone and extracted.get("phone"):
        profile.phone = extracted["phone"]

    github_username = sd.get("github_username")
    github_data = []
    if github_username:
        github_data = await intelligence_engine.fetch_github(github_username)

    final = intelligence_engine.merge_profiles(
        resume_data=extracted,
        linkedin_data=None,
        github_data=github_data
    )
    profile.structured_data = {**(profile.structured_data or {}), **final}
    profile.skills = final.get("skills", profile.skills or [])

    await db.commit()
    await db.refresh(profile)
    return {"status": "extracted", "profile": _serialize(profile)}


# ── Helper ────────────────────────────────────────────────────────────────────

def _serialize(profile: Profile) -> dict:
    sd = profile.structured_data or {}
    return {
        "id": profile.id,
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "location": profile.location,
        "skills": profile.skills or [],
        "summary": profile.summary,
        "links": profile.links or {},
        "structured_data": sd,
        "job_title": sd.get("job_title"),
        "years_experience": sd.get("total_experience_years", 0),
        "education": sd.get("education", []),
        "experience": sd.get("experience", []),
        "projects": sd.get("projects", []),
        "target_roles": sd.get("target_roles", []),
        "preferred_locations": sd.get("preferred_locations", []),
        "remote_preference": sd.get("remote_preference", "Any"),
        "match_threshold": sd.get("match_threshold", 80),
        "github_username": sd.get("github_username"),
        "linkedin_url": sd.get("linkedin_url"),
        "portfolio_url": sd.get("portfolio_url"),
        "resume_variants": profile.resume_variants or {},
        "skill_graph": profile.skill_graph or {},
        "has_resume": bool(profile.raw_resume_text),
    }
