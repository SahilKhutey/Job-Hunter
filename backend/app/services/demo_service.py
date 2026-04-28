from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.job import Job, Application
from app.models.profile import Profile
from app.models.user import User, UserIdentity
from app.auth.utils import hash_password

DEMO_EMAIL = "demo@hunteros.ai"
DEMO_PASSWORD = "demo_password_2026"
DEMO_NAME = "Sahil Khutey"

async def initialize_demo_account(db: AsyncSession):
    """
    Ensures the demo user exists and is fully seeded with realistic data (Async).
    """
    # 1. Setup Demo User
    stmt = select(User).filter(User.email == DEMO_EMAIL)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
            full_name=DEMO_NAME
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        identity = UserIdentity(
            user_id=user.id, 
            full_name=DEMO_NAME,
            emails=[DEMO_EMAIL],
            phone="+1 (555) 123-4567",
            location="San Francisco, CA",
            linkedin_url="https://linkedin.com/in/sahilkhutey",
            github_url="https://github.com/SahilKhutey",
            answers={
                "visa": "Citizen",
                "relocation": "Yes",
                "notice_period": "Immediate",
                "salary_expectation": "$180,000 - $220,000",
                "summary": "Principal AI Architect with expertise in Multi-Agent Systems, Computer Vision, and Distributed Infrastructure.",
                "job_title": "Principal AI Architect",
                "skills": ["Python", "TypeScript", "FastAPI", "React", "Next.js", "PyTorch", "Docker", "Kubernetes", "OpenAI API", "Playwright"],
                "experience": [
                    {
                        "company": "DeepMind",
                        "role": "Senior Research Engineer",
                        "duration": "2022 - Present",
                        "description": "Leading the development of large-scale agentic coding models and autonomous systems."
                    },
                    {
                        "company": "Tesla",
                        "role": "Computer Vision Engineer",
                        "duration": "2020 - 2022",
                        "description": "Optimized perception pipelines for FSD using Vision Transformers and PyTorch."
                    }
                ],
                "education": [
                    {
                        "degree": "M.S. Computer Science (AI Specialization)",
                        "institution": "Stanford University",
                        "year": "2020"
                    }
                ]
            }
        )
        db.add(identity)
        await db.commit()
    
    # 2. Setup Profile
    profile_stmt = select(Profile).filter(Profile.email == DEMO_EMAIL)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalar_one_or_none()

    if not profile:
        profile = Profile(
            email=DEMO_EMAIL,
            full_name=DEMO_NAME,
            summary="Principal AI Architect with expertise in Multi-Agent Systems, Computer Vision, and Distributed Infrastructure.",
            skills=["Python", "TypeScript", "FastAPI", "React", "Next.js", "PyTorch", "Docker", "Kubernetes", "OpenAI API", "Playwright"],
            location="San Francisco, CA",
            raw_resume_text="Sahil Khutey. Principal AI Architect. Expert in building autonomous agent ecosystems..."
        )
        db.add(profile)
        await db.commit()

    # 3. Setup Jobs
    companies = [
        ("NVIDIA", "Senior Deep Learning Engineer", "Santa Clara, CA (Hybrid)", "AI/ML", ["PyTorch", "CUDA", "C++"], "$200k - $300k"),
        ("OpenAI", "Applied AI Researcher", "San Francisco, CA", "Research", ["LLMs", "Python", "Scaling"], "$250k - $450k"),
        ("Google", "Staff Software Engineer, Google Cloud", "Sunnyvale, CA", "Infrastructure", ["Go", "Kubernetes", "Distributed Systems"], "$190k - $280k"),
        ("Anthropic", "Full Stack Engineer (Product)", "San Francisco, CA", "Product", ["Next.js", "React", "Python"], "$180k - $260k"),
        ("Tesla", "Autopilot AI Engineer", "Palo Alto, CA", "Computer Vision", ["C++", "PyTorch", "Vision Transformers"], "$210k - $320k"),
        ("Meta", "Senior Software Engineer (GenAI)", "Menlo Park, CA", "AI", ["PyTorch", "Python", "Distributed Training"], "$220k - $350k"),
        ("Microsoft", "Azure AI Solutions Architect", "Redmond, WA", "Cloud", ["Azure", "Python", "C#"], "$170k - $240k"),
        ("Databricks", "Principal Software Engineer (Data)", "San Francisco, CA", "Data", ["Scala", "Spark", "Java"], "$230k - $400k"),
    ]
    
    for comp, title, loc, source, skills, salary in companies:
        job_stmt = select(Job).filter(Job.company == comp, Job.title == title)
        job_result = await db.execute(job_stmt)
        existing = job_result.scalar_one_or_none()

        if not existing:
            job = Job(
                title=title,
                company=comp,
                location=loc,
                source=source,
                description=f"Join {comp} to build the future of {source}.",
                skills_required=skills,
                salary_range=salary,
                match_score=random.uniform(0.75, 0.98),
                ai_decision="AUTO_APPLY_READY" if random.random() > 0.5 else "REVIEW",
                match_analytics={"match_level": "High", "reasons": ["Skill overlap", "Relevant experience"]}
            )
            db.add(job)
    await db.commit()

    # 4. Applications
    await db.execute(delete(Application).filter(Application.user_id == user.id))
    await db.commit()
    
    jobs_result = await db.execute(select(Job))
    jobs = jobs_result.scalars().all()
    statuses = ["applied", "interview", "offer", "rejected", "shortlisted"]
    
    for i, job in enumerate(jobs):
        status = random.choices(statuses, weights=[0.3, 0.3, 0.1, 0.1, 0.2])[0]
        app = Application(
            user_id=user.id,
            job_id=job.id,
            status=status,
            applied_at=datetime.now() - timedelta(days=random.randint(1, 14)),
            resume_version="Demo_Architect_v1",
            resume_path="/static/resumes/demo_resume.pdf",
            cover_letter="Sample cover letter",
            platform="linkedin",
            applied_match_score=job.match_score
        )
        db.add(app)
    await db.commit()
    
    return user
