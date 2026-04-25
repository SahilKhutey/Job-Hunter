import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal, engine, Base
from app.models.job import Job, Application
from app.models.profile import Profile
from app.models.user import User, UserIdentity
from app.auth.utils import hash_password

DEMO_EMAIL = "demo@hunteros.ai"
DEMO_PASSWORD = "demo_password_2026"
DEMO_NAME = "Sahil Khutey"

def seed_demo_user(db):
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    print(f"Checking for demo user: {DEMO_EMAIL}...")
    user = db.query(User).filter(User.email == DEMO_EMAIL).first()
    if not user:
        print("Creating new demo user...")
        user = User(
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
            full_name=DEMO_NAME
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
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
                "salary_expectation": "$180,000 - $220,000"
            }
        )
        db.add(identity)
        db.commit()
    
    # Create or update profile
    profile = db.query(Profile).filter(Profile.email == DEMO_EMAIL).first()
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
        db.commit()
    
    return user, profile

def seed_professional_jobs(db):
    print("Seeding professional jobs...")
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
    
    jobs = []
    for comp, title, loc, source, skills, salary in companies:
        # Check if job exists
        existing = db.query(Job).filter(Job.company == comp, Job.title == title).first()
        if existing:
            jobs.append(existing)
            continue
            
        job = Job(
            title=title,
            company=comp,
            location=loc,
            source=source,
            description=f"Join {comp} to build the future of {source}. We are looking for an expert in {', '.join(skills)}.",
            skills_required=skills,
            salary_range=salary,
            match_score=random.uniform(0.75, 0.98),
            ai_decision="AUTO_APPLY_READY" if random.random() > 0.5 else "REVIEW"
        )
        db.add(job)
        jobs.append(job)
    
    db.commit()
    return jobs

def simulate():
    db = SessionLocal()
    try:
        # 1. Setup Demo User
        user, profile = seed_demo_user(db)
        
        # 2. Setup Jobs
        jobs = seed_professional_jobs(db)
        
        # 3. Simulate Application History
        print("Simulating application history...")
        db.query(Application).filter(Application.user_id == user.id).delete()
        db.commit()
        
        statuses = ["applied", "interview", "offer", "rejected", "shortlisted"]
        weights = [0.3, 0.3, 0.1, 0.1, 0.2]
        
        for i, job in enumerate(jobs):
            status = random.choices(statuses, weights=weights)[0]
            days_ago = random.randint(1, 14)
            applied_at = datetime.now() - timedelta(days=days_ago)
            
            app = Application(
                user_id=user.id,
                job_id=job.id,
                status=status,
                applied_at=applied_at,
                resume_version="Demo_Architect_v1",
                resume_path="/static/resumes/demo_resume.pdf",
                cover_letter=f"Dear {job.company} Hiring Team,\n\nI am thrilled to apply for the {job.title} position. My background in AI and multi-agent systems aligns perfectly with your requirements...",
                platform="linkedin" if i % 2 == 0 else "company_site"
            )
            db.add(app)
            print(f"  [{i+1}/{len(jobs)}] Application: {job.title} @ {job.company} -> {status}")
            
        db.commit()
        print("\nDemo simulation complete! Dashboard is now hyper-realistic.")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    simulate()
