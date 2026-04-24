from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.db.base_class import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    code = Column(String, nullable=False)
    purpose = Column(String, default="step-up") # e.g., "step-up", "password-reset"
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
