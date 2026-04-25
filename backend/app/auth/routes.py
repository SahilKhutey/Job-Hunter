from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas import UserCreate, UserLogin, TokenResponse
from app.auth.service import register_user, authenticate_user, generate_tokens
from app.core.database import get_db
from app.auth.jwt_handler import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data.email, data.password, data.full_name)
        return generate_tokens(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return generate_tokens(user)


@router.post("/demo", response_model=TokenResponse)
def demo_login(db: Session = Depends(get_db)):
    """
    One-click demo login. Ensures demo user is seeded and returns tokens.
    """
    from app.services.demo_service import initialize_demo_account, DEMO_PASSWORD
    
    # 1. Initialize demo account
    user = initialize_demo_account(db)
    
    # 2. Authenticate (just to be safe/consistent)
    user = authenticate_user(db, user.email, DEMO_PASSWORD)
    
    if not user:
        raise HTTPException(status_code=500, detail="Demo initialization failed")
        
    return generate_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: str):
    from app.auth.jwt_handler import decode_token

    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload["sub"]

    return {
        "access_token": create_access_token({"sub": user_id}),
        "refresh_token": create_refresh_token({"sub": user_id}),
        "token_type": "bearer"
    }
import secrets
from app.auth.dependencies import get_current_user
from app.models.user import User

@router.post("/extension-token")
def generate_extension_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a high-entropy long-lived token for the browser extension."""
    token = "hos_ext_" + secrets.token_urlsafe(32)
    current_user.extension_token = token
    db.commit()
    return {"token": token}
