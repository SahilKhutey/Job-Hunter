from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, Application
from app.models.profile import Profile
from typing import Optional

router = APIRouter()


@router.get("/stats")
def dashboard_stats(
    profile_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Return real application statistics for the dashboard."""
    total_jobs = db.query(Job).count()
    total_applications = db.query(Application).count()

    # Status breakdown
    pending = db.query(Application).filter(Application.status == "pending").count()
    applied = db.query(Application).filter(Application.status == "applied").count()
    interviews = db.query(Application).filter(Application.status == "interview").count()
    offers = db.query(Application).filter(Application.status == "offer").count()
    rejected = db.query(Application).filter(Application.status == "rejected").count()
    responses = applied + interviews + offers  # Any non-pending outcome

    # AI matches
    auto_ready = db.query(Job).filter(Job.ai_decision == "AUTO_APPLY_READY").count()
    review = db.query(Job).filter(Job.ai_decision == "REVIEW").count()

    return {
        "total_jobs_analyzed": total_jobs,
        "total_applications": total_applications,
        "applications_this_week": total_applications,  # Simplified — could filter by date
        "responses": responses,
        "interviews": interviews,
        "offers": offers,
        "ai_matches_above_threshold": auto_ready + review,
        "auto_ready_count": auto_ready,
        "response_rate": round((responses / total_applications * 100), 1) if total_applications > 0 else 0,
        "interview_rate": round((interviews / total_applications * 100), 1) if total_applications > 0 else 0,
        "status_breakdown": {
            "pending": pending,
            "applied": applied,
            "interview": interviews,
            "offer": offers,
            "rejected": rejected,
        }
    }


@router.get("/activity")
def dashboard_activity(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """Return recent activity events."""
    # Get recent applications ordered by applied_at
    recent_apps = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .order_by(Application.applied_at.desc())
        .limit(limit)
        .all()
    )

    events = []
    for app in recent_apps:
        events.append({
            "type": "application",
            "icon": "send",
            "title": f"Application submitted to {app.job.company}",
            "desc": f"{app.job.title} — Status: {app.status.replace('_', ' ').title()}",
            "time": app.applied_at.isoformat() if app.applied_at else "",
        })

    # Get recent high-score jobs (new matches)
    new_matches = (
        db.query(Job)
        .filter(Job.match_score >= 0.80)
        .filter(Job.ai_decision == "AUTO_APPLY_READY")
        .order_by(Job.posted_at.desc())
        .limit(5)
        .all()
    )
    for job in new_matches:
        events.append({
            "type": "match",
            "icon": "auto_awesome",
            "title": f"New Match: {job.company}",
            "desc": f"{job.title} — {round(job.match_score * 100)}% compatibility",
            "time": job.posted_at.isoformat() if job.posted_at else "",
        })

    # Sort by time desc
    events.sort(key=lambda e: e["time"], reverse=True)
    return events[:limit]


@router.get("/top-picks")
def top_picks(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(5),
    db: Session = Depends(get_db)
):
    """Return the top jobs by match score for the dashboard picks widget."""
    jobs = (
        db.query(Job)
        .filter(Job.match_score > 0)
        .order_by(Job.match_score.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "match_score": j.match_score,
            "ai_decision": j.ai_decision,
        }
        for j in jobs
    ]
