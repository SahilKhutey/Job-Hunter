from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.auth.jwt_handler import ALGORITHM
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Check for Extension Token (X-HOS-Extension-Token)
    ext_token = request.headers.get("X-HOS-Extension-Token")
    if ext_token:
        stmt = select(User).filter(User.extension_token == ext_token)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user and user.is_active:
            return user
    
    # 2. Standard OAuth2/JWT logic
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise credentials_exception
        
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user_stmt = select(User).filter(User.id == user_id)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        raise credentials_exception
        
    return user
