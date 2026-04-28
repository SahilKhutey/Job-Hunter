from sqlalchemy import Column, Integer, String, Text, JSON
from app.core.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    
    raw_resume_text = Column(Text)
    structured_data = Column(JSON) # Extracted skills, experience, education
    skills = Column(JSON) # List of skills
    
    summary = Column(Text, nullable=True)
    links = Column(JSON, nullable=True) # LinkedIn, GitHub, etc.
    
    # New Intelligent Pipeline Fields
    resume_variants = Column(JSON, default=dict) # e.g., {"Standard": [...], "AI Engineer": [...]}
    skill_graph = Column(JSON, default=dict) # e.g., {"clusters": [...], "strength": 85}
    preference_weights = Column(JSON, default=lambda: {"skills": 1.0, "experience": 1.0, "education": 1.0, "location": 1.0})

