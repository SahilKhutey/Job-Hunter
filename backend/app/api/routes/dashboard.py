from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, Application
from app.models.profile import Profile
from typing import Optional

router = APIRouter()


from app.services.analytics_service import analytics_service

@router.get("/stats")
def dashboard_stats(
    profile_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Return real application statistics for the dashboard."""
    total_jobs = db.query(Job).count()
    applications = db.query(Application).all()
    
    # Compute base stats
    base_stats = analytics_service.compute_dashboard_stats(applications)
    resume_perf = analytics_service.analyze_resume_performance(applications)
    platform_perf = analytics_service.analyze_platform_performance(applications)
    ai_insights = analytics_service.generate_ai_insights(base_stats, resume_perf, platform_perf)

    # AI matches
    auto_ready = db.query(Job).filter(Job.ai_decision == "AUTO_APPLY_READY").count()
    review = db.query(Job).filter(Job.ai_decision == "REVIEW").count()

    return {
        "total_jobs_analyzed": total_jobs,
        "total_applications": base_stats["total_applications"],
        "responses": sum(1 for a in applications if a.status in ["applied", "interview", "offer"]),
        "interviews": sum(1 for a in applications if a.status == "interview"),
        "offers": sum(1 for a in applications if a.status == "offer"),
        "ai_matches_above_threshold": auto_ready + review,
        "response_rate": base_stats["interview_rate"], # For backward compatibility in UI
        "interview_rate": base_stats["interview_rate"],
        "status_breakdown": base_stats["status_breakdown"],
        "ai_insights": ai_insights,
        "resume_performance": resume_perf,
        "platform_performance": platform_perf
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
