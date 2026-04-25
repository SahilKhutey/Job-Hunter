from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services.intelligence_engine import intelligence_engine
from typing import Dict, Any

router = APIRouter()

@router.post("/analyze")
def extension_analyze(
    payload: Dict[str, Any],
    db: Session = Depends(deps.get_db)
):
    """Analyze a job from the browser extension."""
    job_html = payload.get("html_content")
    if not job_html:
        raise HTTPException(status_code=400, detail="HTML content required")
        
    # In production, we'd extract text from HTML here
    # For demo, we'll assume the extension sends the text directly
    job_text = payload.get("text_content", "Sample Job Description")
    
    # Get user profile for matching (simplified for demo)
    profile = db.query(deps.Profile).first() 
    if not profile:
         raise HTTPException(status_code=404, detail="Profile not found")

    analysis = intelligence_engine.analyze_job_match(job_text, {"skills": profile.skills})
    
    return {
        "match_score": analysis["score"],
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "advice": analysis["upskill_advice"]
    }

@router.post("/sync")
def extension_sync(
    payload: Dict[str, Any],
    db: Session = Depends(deps.get_db)
):
    """Save a job lead from the extension to the main dashboard."""
    # Logic to create a 'Job' record in 'PENDING' status
    return {"status": "success", "message": "Job synced to HunterOS"}
