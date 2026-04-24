from sqlalchemy.orm import Session
from app.models.user import User, UserIdentity
from app.auth.utils import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, create_refresh_token


def register_user(db: Session, email: str, password: str, full_name: str = None):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("User already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Initialize UserIdentity
    identity = UserIdentity(user_id=user.id, full_name=full_name)
    db.add(identity)
    db.commit()

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def generate_tokens(user: User):
    payload = {"sub": str(user.id)}

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }
