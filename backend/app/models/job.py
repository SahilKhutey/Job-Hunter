from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    url = Column(String, unique=True)
    salary_range = Column(String, nullable=True)
    job_type = Column(String, nullable=True) # Full-time, Remote, etc.
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String) # LinkedIn, Indeed, etc.
    
    # Normalized Fields
    skills_required = Column(JSON, default=list)
    experience_required = Column(String, nullable=True)
    
    # AI Decisioning
    match_score = Column(Float, default=0.0)
    ai_decision = Column(String, default="PENDING") # PENDING, AUTO_APPLY_READY, REVIEW, IGNORE
    
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="pending") # pending, applied, interview, rejected, offer
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    
    resume_path = Column(String)
    cover_letter = Column(Text)
    
    job = relationship("Job", back_populates="applications")
