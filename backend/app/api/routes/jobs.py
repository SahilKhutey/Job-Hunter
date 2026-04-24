from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, Application
from app.models.profile import Profile
from typing import Optional

router = APIRouter()


@router.get("")
def list_jobs(
    profile_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    decision: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Return all jobs from the database, optionally filtered by AI decision."""
    query = db.query(Job)
    if decision:
        query = query.filter(Job.ai_decision == decision)
    jobs = query.order_by(Job.match_score.desc()).offset(offset).limit(limit).all()

    profile = None
    if profile_id:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()

    return [_serialize_job(j, profile) for j in jobs]



@router.get("/count")
def count_jobs(db: Session = Depends(get_db)):
    return {"count": db.query(Job).count()}


@router.post("/seed")
def seed_jobs(db: Session = Depends(get_db)):
    """
    Seed the database with real-style job listings for demonstration.
    Each job has a URL, description, and all required fields.
    In production this is replaced by the live job scraper.
    """
    if db.query(Job).count() > 0:
        return {"status": "already_seeded", "count": db.query(Job).count()}

    SEED_JOBS = [
        {"title": "Senior Backend Engineer", "company": "Stripe", "description": "Financial infrastructure scaling...", "location": "San Francisco, CA", "url": "https://stripe.com/jobs/1", "salary_range": "$180k-$250k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Go", "Distributed Systems"], "experience_required": "5+ years", "match_score": 0.95, "ai_decision": "FIT"},
        {"title": "ML Engineer", "company": "OpenAI", "description": "LLM platform engineering...", "location": "San Francisco, CA", "url": "https://openai.com/jobs/2", "salary_range": "$200k-$300k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "PyTorch", "CUDA"], "experience_required": "4+ years", "match_score": 0.88, "ai_decision": "FIT"},
        {"title": "Full Stack Engineer", "company": "Linear", "description": "High-performance productivity tools...", "location": "Remote", "url": "https://linear.app/jobs/3", "salary_range": "$160k-$210k", "job_type": "Remote", "source": "Company Site", "skills_required": ["TypeScript", "React", "Node.js"], "experience_required": "3+ years", "match_score": 0.72, "ai_decision": "MAYBE"},
        {"title": "Software Engineer, Platform", "company": "Vercel", "description": "Edge computing and CDN...", "location": "Remote", "url": "https://vercel.com/jobs/4", "salary_range": "$150k-$200k", "job_type": "Remote", "source": "Company Site", "skills_required": ["TypeScript", "Rust", "Node.js"], "experience_required": "3+ years", "match_score": 0.65, "ai_decision": "MAYBE"},
        {"title": "Backend Engineer", "company": "Notion", "description": "AI-powered productivity...", "location": "New York, NY", "url": "https://notion.com/jobs/5", "salary_range": "$160k-$220k", "job_type": "Hybrid", "source": "Company Site", "skills_required": ["Python", "FastAPI", "PostgreSQL"], "experience_required": "4+ years", "match_score": 0.81, "ai_decision": "FIT"},
        {"title": "Data Engineer", "company": "Airbnb", "description": "Scalable data pipelines...", "location": "San Francisco, CA", "url": "https://airbnb.com/jobs/6", "salary_range": "$170k-$230k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Spark", "Kafka"], "experience_required": "5+ years", "match_score": 0.45, "ai_decision": "NO_FIT"},
        {"title": "ML Infra Engineer", "company": "Anthropic", "description": "AI safety and scaling...", "location": "San Francisco, CA", "url": "https://anthropic.com/jobs/7", "salary_range": "$180k-$280k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "CUDA", "Kubernetes"], "experience_required": "4+ years", "match_score": 0.92, "ai_decision": "FIT"},
        {"title": "Frontend Engineer", "company": "Figma", "description": "Design systems at scale...", "location": "San Francisco, CA", "url": "https://figma.com/jobs/8", "salary_range": "$155k-$215k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["TypeScript", "React", "CSS"], "experience_required": "4+ years", "match_score": 0.58, "ai_decision": "MAYBE"},
        {"title": "DevOps Engineer", "company": "HashiCorp", "description": "Infrastructure as code...", "location": "Remote", "url": "https://hashicorp.com/jobs/9", "salary_range": "$140k-$190k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Go", "Terraform", "AWS"], "experience_required": "4+ years", "match_score": 0.35, "ai_decision": "NO_FIT"},
        {"title": "Security Engineer", "company": "Cloudflare", "description": "Protecting the internet...", "location": "Austin, TX", "url": "https://cloudflare.com/jobs/10", "salary_range": "$150k-$210k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Rust", "Go", "Networking"], "experience_required": "5+ years", "match_score": 0.25, "ai_decision": "NO_FIT"},
        {"title": "Product Engineer", "company": "Retool", "description": "Internal tool builder...", "location": "San Francisco, CA", "url": "https://retool.com/jobs/11", "salary_range": "$160k-$220k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["TypeScript", "React", "PostgreSQL"], "experience_required": "3+ years", "match_score": 0.78, "ai_decision": "FIT"},
        {"title": "Systems Engineer", "company": "Cloudflare", "description": "Distributed systems at edge...", "location": "Lisbon, Portugal", "url": "https://cloudflare.com/jobs/12", "salary_range": "€80k-€120k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Rust", "C++", "Networking"], "experience_required": "5+ years", "match_score": 0.15, "ai_decision": "NO_FIT"},
        {"title": "iOS Engineer", "company": "Uber", "description": "Mobile architecture...", "location": "San Francisco, CA", "url": "https://uber.com/jobs/13", "salary_range": "$170k-$240k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Swift", "Objective-C", "Mobile"], "experience_required": "4+ years", "match_score": 0.05, "ai_decision": "NO_FIT"},
        {"title": "Android Engineer", "company": "DoorDash", "description": "Food delivery mobile...", "location": "Remote", "url": "https://doordash.com/jobs/14", "salary_range": "$160k-$220k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Kotlin", "Java", "Mobile"], "experience_required": "4+ years", "match_score": 0.08, "ai_decision": "NO_FIT"},
        {"title": "Rust Developer", "company": "Discord", "description": "High-performance chat backend...", "location": "San Francisco, CA", "url": "https://discord.com/jobs/15", "salary_range": "$180k-$250k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Rust", "Elixir", "Distributed Systems"], "experience_required": "5+ years", "match_score": 0.42, "ai_decision": "MAYBE"},
        {"title": "QA Automation Engineer", "company": "Datadog", "description": "Monitoring and observability...", "location": "Paris, France", "url": "https://datadog.com/jobs/16", "salary_range": "€70k-€100k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Selenium", "Docker"], "experience_required": "3+ years", "match_score": 0.32, "ai_decision": "NO_FIT"},
        {"title": "Technical Writer", "company": "Postman", "description": "API documentation...", "location": "Remote", "url": "https://postman.com/jobs/17", "salary_range": "$100k-$140k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Technical Writing", "APIs", "Markdown"], "experience_required": "2+ years", "match_score": 0.22, "ai_decision": "NO_FIT"},
        {"title": "Product Designer", "company": "Intercom", "description": "Customer messaging design...", "location": "Dublin, Ireland", "url": "https://intercom.com/jobs/18", "salary_range": "€90k-€130k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Product Design", "Figma", "UI/UX"], "experience_required": "4+ years", "match_score": 0.02, "ai_decision": "NO_FIT"},
        {"title": "Senior Solutions Architect", "company": "AWS", "description": "Cloud migration and strategy...", "location": "Seattle, WA", "url": "https://aws.amazon.com/jobs/19", "salary_range": "$180k-$260k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Cloud Computing", "AWS", "Architecture"], "experience_required": "8+ years", "match_score": 0.48, "ai_decision": "MAYBE"},
        {"title": "Data Scientist", "company": "Spotify", "description": "Music recommendation models...", "location": "Stockholm, Sweden", "url": "https://spotify.com/jobs/20", "salary_range": "800k-1M SEK", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "SQL", "Machine Learning"], "experience_required": "3+ years", "match_score": 0.55, "ai_decision": "MAYBE"},
        {"title": "Staff Engineer", "company": "Slack", "description": "Enterprise messaging scale...", "location": "San Francisco, CA", "url": "https://slack.com/jobs/21", "salary_range": "$220k-$320k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Java", "PHP", "Distributed Systems"], "experience_required": "10+ years", "match_score": 0.62, "ai_decision": "MAYBE"},
        {"title": "VP of Engineering", "company": "StartupX", "description": "Scaling early stage team...", "location": "Remote", "url": "https://startupx.com/jobs/22", "salary_range": "$250k-$350k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Leadership", "Hiring", "Product Strategy"], "experience_required": "12+ years", "match_score": 0.41, "ai_decision": "NO_FIT"},
        {"title": "Founding Engineer", "company": "AI-Studio", "description": "Building the next generation AI tool...", "location": "London, UK", "url": "https://aistudio.com/jobs/23", "salary_range": "£80k-£120k + Equity", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Python", "Next.js", "AI"], "experience_required": "4+ years", "match_score": 0.85, "ai_decision": "FIT"},
        {"title": "Senior AI Researcher", "company": "Mistral AI", "description": "Open source LLM research...", "location": "Paris, France", "url": "https://mistral.ai/jobs/24", "salary_range": "€120k-€180k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Deep Learning", "LLMs", "NLP"], "experience_required": "6+ years", "match_score": 0.79, "ai_decision": "FIT"},
        {"title": "Cloud Platform Engineer", "company": "GCP", "description": "Building the future of cloud computing...", "location": "Mountain View, CA", "url": "https://google.com/jobs/25", "salary_range": "$180k-$250k", "job_type": "Full-time", "source": "Company Site", "skills_required": ["Go", "Kubernetes", "GCP"], "experience_required": "5+ years", "match_score": 0.71, "ai_decision": "MAYBE"},
        {"title": "Senior SRE", "company": "GitHub", "description": "Reliability for the home of developers...", "location": "Remote", "url": "https://github.com/jobs/26", "salary_range": "$170k-$230k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Ruby", "Go", "Infrastructure"], "experience_required": "6+ years", "match_score": 0.52, "ai_decision": "MAYBE"},
        {"title": "Backend Lead", "company": "Brex", "description": "Fintech platform for startups...", "location": "Remote", "url": "https://brex.com/jobs/27", "salary_range": "$200k-$280k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Elixir", "PostgreSQL", "Systems Design"], "experience_required": "7+ years", "match_score": 0.44, "ai_decision": "NO_FIT"},
        {"title": "Senior Software Engineer", "company": "Supabase", "description": "Building the open source Firebase...", "location": "Remote", "url": "https://supabase.com/jobs/28", "salary_range": "$160k-$220k", "job_type": "Remote", "source": "Company Site", "skills_required": ["PostgreSQL", "Go", "Elixir"], "experience_required": "5+ years", "match_score": 0.68, "ai_decision": "MAYBE"},
        {"title": "Full Stack Dev", "company": "Railway", "description": "Deployment made easy...", "location": "Remote", "url": "https://railway.app/jobs/29", "salary_range": "$150k-$210k", "job_type": "Remote", "source": "Company Site", "skills_required": ["TypeScript", "Next.js", "Docker"], "experience_required": "3+ years", "match_score": 0.75, "ai_decision": "FIT"},
        {"title": "Senior Engineer", "company": "Neon", "description": "Serverless Postgres...", "location": "Remote", "url": "https://neon.tech/jobs/30", "salary_range": "$170k-$240k", "job_type": "Remote", "source": "Company Site", "skills_required": ["Rust", "PostgreSQL", "Systems"], "experience_required": "5+ years", "match_score": 0.59, "ai_decision": "MAYBE"},
    ]

    created = []
    for j in SEED_JOBS:
        job = Job(**j)
        db.add(job)
        created.append(j["title"])

    db.commit()
    return {"status": "seeded", "count": len(created), "jobs": created}


def _serialize_job(j: Job, profile: Optional[Profile] = None) -> dict:
    from app.services.matching_service import matching_service
    
    metrics = {
        "match_score": j.match_score or 0.0,
        "difficulty": 0.5,
        "priority": "MEDIUM",
        "skill_gap": []
    }
    
    if profile:
        metrics = matching_service.calculate_metrics(profile, j)

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
        "posted_at": j.posted_at.isoformat() if j.posted_at else None,
        **metrics
    }

