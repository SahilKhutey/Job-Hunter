from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User # Added to resolve relationship mapping

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
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    status = Column(String, default="applied") # applied, shortlisted, interview, rejected, offer
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    
    resume_version = Column(String) # e.g. "Full-Stack_v1", "Tailored_JS_JD123"
    resume_path = Column(String)
    cover_letter = Column(Text)
    
    platform = Column(String) # linkedin, indeed, company_site
    
    # Store extra signals (e.g. why we applied, score at time of application)
    application_metadata = Column(JSON, default=dict)
    
    job = relationship("Job", back_populates="applications")
    user = relationship("User", back_populates="applications")

