from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.models.user import User, UserIdentity
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def read_user_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active
    }

@router.get("/identity")
def get_user_identity(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Fetch the core user identity linked to the logged-in user.
    """
    identity = db.query(UserIdentity).filter(UserIdentity.user_id == current_user.id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    
    return {
        "full_name": identity.full_name,
        "emails": identity.emails,
        "phone": identity.phone,
        "location": identity.location,
        "answers": identity.answers,
        "links": {
            "linkedin": identity.linkedin_url,
            "github": identity.github_url,
            "portfolio": identity.portfolio_url
        }
    }

@router.post("/identity")
def update_user_identity(data: Dict[str, Any], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Update the core user identity.
    """
    identity = db.query(UserIdentity).filter(UserIdentity.user_id == current_user.id).first()
    if not identity:
        identity = UserIdentity(user_id=current_user.id)
        db.add(identity)

    for key, value in data.items():
        if hasattr(identity, key):
            setattr(identity, key, value)
    
    # Handle links specifically if they are nested in data
    if "links" in data:
        links = data["links"]
        identity.linkedin_url = links.get("linkedin", identity.linkedin_url)
        identity.github_url = links.get("github", identity.github_url)
        identity.portfolio_url = links.get("portfolio", identity.portfolio_url)

    db.commit()
    return {"status": "success", "message": "Identity updated successfully."}
