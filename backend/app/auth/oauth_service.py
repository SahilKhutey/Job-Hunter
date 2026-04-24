from sqlalchemy.orm import Session
from app.models.user import User, UserIdentity

def get_or_create_oauth_user(db: Session, email: str, provider: str, provider_id: str, full_name: str = None):
    user = db.query(User).filter(User.email == email).first()

    if user:
        # Update provider info if not set
        if not user.provider:
            user.provider = provider
            user.provider_id = provider_id
            db.commit()
        return user

    user = User(
        email=email,
        provider=provider,
        provider_id=provider_id,
        full_name=full_name,
        hashed_password=""  # Not needed for OAuth users
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Initialize UserIdentity
    identity = UserIdentity(user_id=user.id, full_name=full_name)
    db.add(identity)
    db.commit()

    return user
