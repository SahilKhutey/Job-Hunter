from sqlalchemy.orm import Session
from app.models.user import UserIdentity, Credential
from app.utils.vault import vault
from typing import Dict, Any, Optional

class IdentityService:
    @staticmethod
    def get_identity(db: Session, identity_id: int = 1) -> Optional[UserIdentity]:
        return db.query(UserIdentity).filter(UserIdentity.id == identity_id).first()

    @staticmethod
    def update_identity(db: Session, identity_id: int, data: Dict[str, Any]) -> UserIdentity:
        identity = db.query(UserIdentity).filter(UserIdentity.id == identity_id).first()
        if not identity:
            identity = UserIdentity(id=identity_id)
            db.add(identity)
        
        for key, value in data.items():
            if hasattr(identity, key) and key != "id":
                setattr(identity, key, value)
        
        db.commit()
        db.refresh(identity)
        return identity

    @staticmethod
    def save_credential(db: Session, platform: str, username: str, password: str) -> Credential:
        encrypted_pw = vault.encrypt(password)
        credential = db.query(Credential).filter(Credential.platform == platform, Credential.username == username).first()
        
        if credential:
            credential.encrypted_password = encrypted_pw
        else:
            credential = Credential(platform=platform, username=username, encrypted_password=encrypted_pw)
            db.add(credential)
            
        db.commit()
        return credential

    @staticmethod
    def get_credential(db: Session, platform: str) -> Optional[Dict[str, Any]]:
        credential = db.query(Credential).filter(Credential.platform == platform).first()
        if not credential:
            return None
        
        return {
            "platform": credential.platform,
            "username": credential.username,
            "password": vault.decrypt(credential.encrypted_password),
            "storage_state": credential.storage_state
        }

identity_service = IdentityService()
