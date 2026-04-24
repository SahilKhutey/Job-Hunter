from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx

from app.auth.oauth_config import oauth
from app.auth.oauth_service import get_or_create_oauth_user
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.core.database import get_db

router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to retrieve user info from Google")

        user = get_or_create_oauth_user(
            db,
            email=user_info["email"],
            provider="google",
            provider_id=user_info["sub"],
            full_name=user_info.get("name")
        )

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        return RedirectResponse(
            url=f"http://localhost:3000/oauth-success?access={access}&refresh={refresh}"
        )
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:3000/login?error={str(e)}")

@router.get("/linkedin")
async def linkedin_login(request: Request):
    redirect_uri = request.url_for("linkedin_callback")
    return await oauth.linkedin.authorize_redirect(request, redirect_uri)

@router.get("/linkedin/callback")
async def linkedin_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.linkedin.authorize_access_token(request)
        
        async with httpx.AsyncClient() as client:
            # Fetch profile
            profile_res = await client.get(
                "https://api.linkedin.com/v2/me",
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            profile_data = profile_res.json()
            
            # Fetch email
            email_res = await client.get(
                "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            email_data = email_res.json()
            email = email_data["elements"][0]["handle~"]["emailAddress"]

        user = get_or_create_oauth_user(
            db,
            email=email,
            provider="linkedin",
            provider_id=profile_data["id"],
            full_name=f"{profile_data.get('localizedFirstName', '')} {profile_data.get('localizedLastName', '')}".strip()
        )

        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        return RedirectResponse(
            url=f"http://localhost:3000/oauth-success?access={access}&refresh={refresh}"
        )
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:3000/login?error={str(e)}")
