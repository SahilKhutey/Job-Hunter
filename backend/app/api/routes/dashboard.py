from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.job import Job, Application
from app.models.profile import Profile
from typing import Optional, List
from app.services.analytics_service import analytics_service

router = APIRouter()

@router.get("/stats")
async def dashboard_stats(
    profile_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Return real application statistics for the dashboard (Async)."""
    # 1. All Jobs (for risk analysis)
    jobs_result = await db.execute(select(Job))
    jobs = jobs_result.scalars().all()
    total_jobs = len(jobs)

    # 2. All Applications
    apps_result = await db.execute(select(Application))
    applications = apps_result.scalars().all()
    
    # Compute base stats via service
    base_stats = analytics_service.compute_dashboard_stats(applications, jobs)
    resume_perf = analytics_service.analyze_resume_performance(applications)
    platform_perf = analytics_service.analyze_platform_performance(applications)
    score_corr = analytics_service.analyze_score_correlation(applications)
    
    ai_insights = analytics_service.generate_ai_insights(base_stats, resume_perf, platform_perf, score_corr)

    # 3. AI Matches (Filtered)
    auto_ready_result = await db.execute(select(func.count(Job.id)).filter(Job.ai_decision == "AUTO_APPLY_READY"))
    auto_ready = auto_ready_result.scalar() or 0
    
    review_result = await db.execute(select(func.count(Job.id)).filter(Job.ai_decision == "REVIEW"))
    review = review_result.scalar() or 0

    return {
        "total_jobs_analyzed": total_jobs,
        "total_applications": base_stats["total_applications"],
        "responses": sum(1 for a in applications if a.status in ["applied", "interview", "offer"]),
        "interviews": sum(1 for a in applications if a.status == "interview"),
        "offers": sum(1 for a in applications if a.status == "offer"),
        "ai_matches_above_threshold": auto_ready + review,
        "risks_avoided": base_stats.get("risks_avoided", 0),
        "response_rate": base_stats["interview_rate"],
        "interview_rate": base_stats["interview_rate"],
        "status_breakdown": base_stats["status_breakdown"],
        "ai_insights": ai_insights,
        "resume_performance": resume_perf,
        "platform_performance": platform_perf,
        "score_correlation": score_corr
    }

@router.get("/activity")
async def dashboard_activity(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    """Return recent activity events (Async)."""
    # Get recent applications ordered by applied_at
    # We join with Job to get company/title
    stmt = (
        select(Application)
        .options(selectinload(Application.job))
        .order_by(desc(Application.applied_at))
        .limit(limit)
    )
    result = await db.execute(stmt)
    recent_apps = result.scalars().all()

    events = []
    for app in recent_apps:
        # Load job relationship if not already loaded (eager loading preferred)
        # For simplicity in this session, we assume join+select worked
        events.append({
            "type": "application",
            "icon": "send",
            "title": f"Application submitted to {app.job.company}",
            "desc": f"{app.job.title} — Status: {app.status.replace('_', ' ').title()}",
            "time": app.applied_at.isoformat() if app.applied_at else "",
        })

    # Get recent high-score jobs (new matches)
    match_stmt = (
        select(Job)
        .filter(Job.match_score >= 0.80)
        .filter(Job.ai_decision == "AUTO_APPLY_READY")
        .order_by(desc(Job.posted_at))
        .limit(5)
    )
    match_result = await db.execute(match_stmt)
    new_matches = match_result.scalars().all()

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
async def top_picks(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(5),
    db: AsyncSession = Depends(get_db)
):
    """Return the top jobs by match score for the dashboard picks widget (Async)."""
    stmt = (
        select(Job)
        .filter(Job.match_score > 0)
        .order_by(desc(Job.match_score))
        .limit(limit)
    )
    result = await db.execute(stmt)
    jobs = result.scalars().all()

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
