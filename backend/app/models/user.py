from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    provider = Column(String, nullable=True)  # google / linkedin
    provider_id = Column(String, nullable=True)

    
    # Relationships
    identity = relationship("UserIdentity", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
    credentials = relationship("Credential", back_populates="user")


class UserIdentity(Base):
    __tablename__ = "user_identities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    full_name = Column(String)
    emails = Column(JSON) # List of emails
    phone = Column(String)
    location = Column(String)
    
    # Common job application answers
    answers = Column(JSON) # e.g., {"visa": "...", "relocation": "..."}
    
    # Links
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)

    # Relationship
    user = relationship("User", back_populates="identity")

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String) # e.g., "LinkedIn", "Indeed"

    username = Column(String)
    encrypted_password = Column(String)
    
    # Session data (stored as JSON)
    storage_state = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="credentials")

