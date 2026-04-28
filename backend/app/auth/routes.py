from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import secrets

from app.auth.schemas import UserCreate, UserLogin, TokenResponse
from app.auth.service import register_user, authenticate_user, generate_tokens
from app.core.database import get_db
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registers a new user (Async)."""
    try:
        user = await register_user(db, data.email, data.password, data.full_name)
        return generate_tokens(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticates a user and returns tokens (Async)."""
    user = await authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return generate_tokens(user)


@router.post("/demo", response_model=TokenResponse)
async def demo_login(db: AsyncSession = Depends(get_db)):
    """
    One-click demo login (Async). Ensures demo user is seeded and returns tokens.
    """
    from app.services.demo_service import initialize_demo_account, DEMO_PASSWORD
    
    # 1. Initialize demo account
    user = await initialize_demo_account(db)
    
    # 2. Authenticate
    user = await authenticate_user(db, user.email, DEMO_PASSWORD)
    
    if not user:
        raise HTTPException(status_code=500, detail="Demo initialization failed")
        
    return generate_tokens(user)

# ... (refresh route remains mostly same as it doesn't use DB directly)

@router.post("/extension-token")
async def generate_extension_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a high-entropy long-lived token for the browser extension (Async)."""
    token = "hos_ext_" + secrets.token_urlsafe(32)
    current_user.extension_token = token
    await db.commit()
    return {"token": token}
