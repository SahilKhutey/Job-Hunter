import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exc
from app.models.user import User, UserIdentity
from app.models.job import Job
from app.models.profile import Profile

@pytest.mark.asyncio
async def test_user_email_uniqueness(async_db: AsyncSession):
    """Verify that email uniqueness is enforced at the DB level."""
    u1 = User(email="elite@hunteros.ai", hashed_password="pw1")
    async_db.add(u1)
    await async_db.commit()
    
    u2 = User(email="elite@hunteros.ai", hashed_password="pw2")
    async_db.add(u2)
    
    with pytest.raises(exc.IntegrityError):
        await async_db.commit()
    await async_db.rollback()

@pytest.mark.asyncio
async def test_job_mandatory_fields(async_db: AsyncSession):
    """Verify that required fields are enforced."""
    # Title is missing
    j1 = Job(company="Test Corp", description="No Title Job")
    async_db.add(j1)
    
    with pytest.raises(exc.IntegrityError):
        await async_db.commit()
    await async_db.rollback()

@pytest.mark.asyncio
async def test_user_identity_relationship_integrity(async_db: AsyncSession):
    """Verify that UserIdentity correctly links to User."""
    user = User(email="rel@hunteros.ai", hashed_password="pw")
    async_db.add(user)
    await async_db.commit()
    
    identity = UserIdentity(user_id=user.id, full_name="Relational Hunter")
    async_db.add(identity)
    await async_db.commit()
    
    # Query back
    stmt = select(UserIdentity).filter(UserIdentity.user_id == user.id)
    result = await async_db.execute(stmt)
    fetched = result.scalar_one()
    assert fetched.full_name == "Relational Hunter"
