import asyncio
import sys
import os
from sqlalchemy.orm import Session

# Add backend to path
sys.path.append(os.getcwd())

from app.agents.application_agent import ApplicationAgent
from app.core.database import SessionLocal, Base, engine

async def test_flow():
    # Setup DB
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    user_id = "test_user_123"
    profile = {
        "full_name": "Antigravity Test",
        "email": "test@example.com",
        "phone": "1234567890",
        "summary": "I am an AI agent testing a multi-step form.",
        "skills": ["Python", "Playwright", "FastAPI"]
    }
    
    agent = ApplicationAgent(user_id, profile, db)
    
    print("--- Starting Multi-Step Test ---")
    success = await agent.apply(
        job_id=999,
        job_url="http://127.0.0.1:8001/",
        tailored_resume_path="static/resumes/default_resume.pdf"
    )
    
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    db.close()

if __name__ == "__main__":
    asyncio.run(test_flow())
