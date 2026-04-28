from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.profile import Profile
from app.services.intelligence_engine import intelligence_engine
from typing import Dict, Any

router = APIRouter()

@router.post("/analyze")
async def extension_analyze(
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Analyze a job from the browser extension."""
    job_text = payload.get("text_content", "Sample Job Description")
    
    # Get user profile for matching
    stmt = select(Profile).limit(1)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    
    if not profile:
         raise HTTPException(status_code=404, detail="Profile not found")

    # intelligence_engine.analyze_job_match is async
    analysis = await intelligence_engine.analyze_job_match(job_text, {"skills": profile.skills or []})
    
    return {
        "match_score": analysis.get("score", 0),
        "matched_skills": analysis.get("matched_skills", []),
        "missing_skills": analysis.get("missing_skills", []),
        "advice": analysis.get("upskill_advice", "")
    }

from app.models.job import Job

@router.post("/sync")
async def extension_sync(
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Save a job lead from the extension to the main dashboard."""
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Job URL is required")
        
    # Check for existing job
    stmt = select(Job).filter(Job.url == url)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        return {"status": "exists", "job_id": existing.id, "message": "Job already in dashboard"}
        
    # Create new job lead
    new_job = Job(
        title=payload.get("title", "Unknown Title"),
        company=payload.get("company", "Unknown Company"),
        url=url,
        description=payload.get("description", ""),
        location=payload.get("location", ""),
        source="Browser Extension",
        ai_decision="PENDING"
    )
    
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    
    return {"status": "success", "job_id": new_job.id, "message": "Job synced to HunterOS"}
