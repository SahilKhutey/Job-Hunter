from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.job import Application
from app.services.analytics_service import analytics_service

from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/analytics", tags=["Dashboard Intelligence"])

@router.get("/dashboard")
async def get_analytics_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns high-level statistics and performance analysis for the user's applications (Async).
    """
    stmt = select(Application).filter(Application.user_id == current_user.id).options(selectinload(Application.job))
    result = await db.execute(stmt)
    applications = result.scalars().all()
    
    stats = analytics_service.compute_dashboard_stats(applications)
    resume_perf = analytics_service.analyze_resume_performance(applications)
    platform_perf = analytics_service.analyze_platform_performance(applications)
    score_corr = analytics_service.analyze_score_correlation(applications)
    
    insights = analytics_service.generate_ai_insights(stats, resume_perf, platform_perf, score_corr)
    
    return {
        "stats": stats,
        "resume_performance": resume_perf,
        "platform_performance": platform_perf,
        "score_correlation": score_corr,
        "insights": insights,
        "recent_applications": [
            {
                "id": app.id,
                "job_title": app.job.title if app.job else "Unknown",
                "company": app.job.company if app.job else "Unknown",
                "status": app.status,
                "applied_at": app.applied_at,
                "platform": app.platform
            } for app in applications[-5:] # Last 5
        ]
    }
