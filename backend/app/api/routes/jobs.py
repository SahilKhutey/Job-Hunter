from fastapi import APIRouter, Depends, Query
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.core.database import get_db
from app.models.job import Job
from app.models.profile import Profile
from typing import Optional, List

router = APIRouter()

@router.get("")
async def list_jobs(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    decision: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Return all jobs from the database (Async)."""
    stmt = select(Job)
    if decision:
        stmt = stmt.filter(Job.ai_decision == decision)
    
    stmt = stmt.order_by(desc(Job.match_score)).offset(offset).limit(limit)
    
    result = await db.execute(stmt)
    jobs = result.scalars().all()

    profile = None
    if profile_id:
        profile_stmt = select(Profile).filter(Profile.id == profile_id)
        profile_result = await db.execute(profile_stmt)
        profile = profile_result.scalar_one_or_none()

    tasks = [_serialize_job(j, profile) for j in jobs]
    return await asyncio.gather(*tasks)

@router.get("/count")
async def count_jobs(db: AsyncSession = Depends(get_db)):
    """Count all jobs (Async)."""
    result = await db.execute(select(func.count(Job.id)))
    return {"count": result.scalar() or 0}

@router.post("/seed")
async def seed_jobs(db: AsyncSession = Depends(get_db)):
    """
    Seed the database with real-style job listings (Async).
    """
    count_result = await db.execute(select(func.count(Job.id)))
    if (count_result.scalar() or 0) > 0:
        return {"status": "already_seeded", "count": count_result.scalar()}

    SEED_JOBS = [
        {"title": "Senior Backend Engineer", "company": "Stripe", "description": "Financial infrastructure scaling...", "location": "San Francisco, CA", "url": "https://stripe.com/jobs/1", "salary_range": "$180k-$250k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Go", "Distributed Systems"], "experience_required": "5+ years", "match_score": 0.95, "ai_decision": "FIT", "red_flags": [], "strategic_risk_score": 5.0, "priority_index": "HIGH"},
        {"title": "ML Engineer", "company": "OpenAI", "description": "LLM platform engineering...", "location": "San Francisco, CA", "url": "https://openai.com/jobs/2", "salary_range": "$200k-$300k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "PyTorch", "CUDA"], "experience_required": "4+ years", "match_score": 0.88, "ai_decision": "FIT", "red_flags": ["High Bar"], "strategic_risk_score": 15.0, "priority_index": "HIGH"},
        {"title": "Full Stack Engineer", "company": "Linear", "description": "High-performance productivity tools...", "location": "Remote", "url": "https://linear.app/jobs/3", "salary_range": "$160k-$210k", "job_type": "Remote", "source": "Company Site", "skills_required": ["TypeScript", "React", "Node.js"], "experience_required": "3+ years", "match_score": 0.72, "ai_decision": "MAYBE", "red_flags": [], "strategic_risk_score": 10.0, "priority_index": "MEDIUM"},
        {"title": "Backend Engineer", "company": "Notion", "description": "AI-powered productivity...", "location": "New York, NY", "url": "https://notion.com/jobs/5", "salary_range": "$160k-$220k", "job_type": "Hybrid", "source": "Company Site", "skills_required": ["Python", "FastAPI", "PostgreSQL"], "experience_required": "4+ years", "match_score": 0.81, "ai_decision": "FIT", "red_flags": [], "strategic_risk_score": 12.0, "priority_index": "MEDIUM"},
        {"title": "Data Engineer", "company": "Airbnb", "description": "Scalable data pipelines...", "location": "San Francisco, CA", "url": "https://airbnb.com/jobs/6", "salary_range": "$170k-$230k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Spark", "Kafka"], "experience_required": "5+ years", "match_score": 0.45, "ai_decision": "NO_FIT", "red_flags": ["Ghost Posting Likely", "Vague Req"], "strategic_risk_score": 65.0, "priority_index": "LOW"},
    ]

    created = []
    for j in SEED_JOBS:
        job = Job(**j)
        db.add(job)
        created.append(j["title"])

    await db.commit()
    return {"status": "seeded", "count": len(created), "jobs": created}

async def _serialize_job(j: Job, profile: Optional[Profile] = None) -> dict:
    from app.services.matching_service import matching_service
    
    metrics = {
        "match_score": j.match_score or 0.0,
        "difficulty": 0.5,
        "priority": "MEDIUM",
        "skill_gap": []
    }
    
    if profile:
        metrics = await matching_service.calculate_metrics(profile, j)

    return {
        "id": j.id,
        "title": j.title,
        "company": j.company,
        "description": j.description,
        "location": j.location,
        "url": j.url,
        "salary_range": j.salary_range,
        "job_type": j.job_type,
        "source": j.source,
        "skills_required": j.skills_required or [],
        "experience_required": j.experience_required,
        "ai_decision": j.ai_decision or "PENDING",
        "red_flags": j.red_flags or [],
        "strategic_risk_score": j.strategic_risk_score or 0.0,
        "priority_index": j.priority_index or "MEDIUM",
        "posted_at": j.posted_at.isoformat() if j.posted_at else None,
        **metrics
    }
