import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models.job import Job, Application
from app.models.profile import Profile

def simulate():
    db = SessionLocal()
    try:
        # Clear existing data for a fresh start
        print("Clearing existing data...")
        db.query(Application).delete()
        db.query(Job).delete()
        db.commit()
        
        # Re-seed jobs using the API logic
        from app.api.routes.jobs import seed_jobs
        seed_jobs(db)
        
        # 1. Get all jobs
        jobs = db.query(Job).all()
        if not jobs:
            print("No jobs found. Please seed jobs first.")
            return
        
        # Update some jobs to have interesting AI decisions
        for i, job in enumerate(jobs):
            if i % 3 == 0:
                job.ai_decision = "AUTO_APPLY_READY"
            elif i % 3 == 1:
                job.ai_decision = "REVIEW"
            else:
                job.ai_decision = "FIT"
        
        # 2. Simulate Applications
        print("Simulating application history...")
        
        # Statuses matching dashboard routes
        statuses = ["pending", "applied", "interview", "offer", "rejected"]
        
        # Select 25 random jobs to have applications
        sampled_jobs = random.sample(jobs, min(25, len(jobs)))
        
        for i, job in enumerate(sampled_jobs):
            # Check if application already exists
            existing = db.query(Application).filter(Application.job_id == job.id).first()
            if existing:
                continue
                
            # Random status with weightage
            status = random.choices(statuses, weights=[0.2, 0.4, 0.2, 0.05, 0.15])[0]
            
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            applied_at = datetime.now() - timedelta(days=days_ago)
            
            app = Application(
                job_id=job.id,
                status=status,
                applied_at=applied_at,
                resume_path="/simulated/resumes/standard.pdf",
                cover_letter="This is a simulated cover letter for testing purposes."
            )
            db.add(app)
            print(f"  [{i+1}/25] Added application: {job.title} at {job.company} ({status})")
            
        db.commit()
        print("\nSimulation complete! 25 diverse applications seeded.")
        print("Dashboard stats and activity feed are now fully populated.")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    simulate()
