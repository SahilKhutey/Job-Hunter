from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import UserIdentity, Credential
from app.utils.vault import vault
from typing import Dict, Any, Optional

class IdentityService:
    @staticmethod
    async def get_identity(db: AsyncSession, identity_id: int = 1) -> Optional[UserIdentity]:
        stmt = select(UserIdentity).filter(UserIdentity.id == identity_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_identity(db: AsyncSession, identity_id: int, data: Dict[str, Any]) -> UserIdentity:
        stmt = select(UserIdentity).filter(UserIdentity.id == identity_id)
        result = await db.execute(stmt)
        identity = result.scalar_one_or_none()
        
        if not identity:
            identity = UserIdentity(id=identity_id)
            db.add(identity)
        
        for key, value in data.items():
            if hasattr(identity, key) and key != "id":
                setattr(identity, key, value)
        
        await db.commit()
        await db.refresh(identity)
        return identity

    @staticmethod
    async def save_credential(db: AsyncSession, platform: str, username: str, password: str) -> Credential:
        encrypted_pw = vault.encrypt(password)
        stmt = select(Credential).filter(Credential.platform == platform, Credential.username == username)
        result = await db.execute(stmt)
        credential = result.scalar_one_or_none()
        
        if credential:
            credential.encrypted_password = encrypted_pw
        else:
            credential = Credential(platform=platform, username=username, encrypted_password=encrypted_pw)
            db.add(credential)
            
        await db.commit()
        return credential

    @staticmethod
    async def get_credential(db: AsyncSession, platform: str) -> Optional[Dict[str, Any]]:
        stmt = select(Credential).filter(Credential.platform == platform)
        result = await db.execute(stmt)
        credential = result.scalar_one_or_none()
        
        if not credential:
            return None
        
        return {
            "platform": credential.platform,
            "username": credential.username,
            "password": vault.decrypt(credential.encrypted_password),
            "storage_state": credential.storage_state
        }

identity_service = IdentityService()
