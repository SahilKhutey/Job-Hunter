from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserIdentity
from app.auth.utils import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, create_refresh_token


async def register_user(db: AsyncSession, email: str, password: str, full_name: str = None):
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise Exception("User already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Initialize UserIdentity
    identity = UserIdentity(user_id=user.id, full_name=full_name)
    db.add(identity)
    await db.commit()

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def generate_tokens(user: User):
    payload = {"sub": str(user.id)}

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }
