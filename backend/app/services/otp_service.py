import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTP

class OTPService:
    @staticmethod
    def generate_code() -> str:
        return str(random.randint(100000, 999999))

    @staticmethod
    def create_otp(db: Session, user_id: str, purpose: str = "step-up") -> str:
        code = OTPService.generate_code()
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        
        otp = OTP(
            id=str(uuid.uuid4()),
            user_id=user_id,
            code=code,
            purpose=purpose,
            expires_at=expires_at
        )
        db.add(otp)
        db.commit()
        return code

    @staticmethod
    def verify_otp(db: Session, user_id: str, code: str, purpose: str = "step-up") -> bool:
        otp = db.query(OTP).filter(
            OTP.user_id == user_id,
            OTP.code == code,
            OTP.purpose == purpose,
            OTP.is_used == False,
            OTP.expires_at > datetime.utcnow()
        ).first()
        
        if otp:
            otp.is_used = True
            db.commit()
            return True
        return False
