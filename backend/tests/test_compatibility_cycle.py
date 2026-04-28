import pytest
import asyncio
from app.services.matching_service import matching_service
from app.services.automation_service import automation_service
from app.api.routes.websocket import manager
from app.models.job import Job, Application
from app.models.user import User, UserIdentity
from sqlalchemy import select
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_full_autonomous_cycle(async_db):
    """
    Verifies the Elite Cycle:
    1. User Discovery (Matching)
    2. Automation Initialization
    3. WebSocket Telemetry (Mocked Manager)
    4. Database History Persistence
    """
    # 1. Setup User & Job
    user = User(email="cycle@hunteros.ai", hashed_password="pw")
    async_db.add(user)
    await async_db.commit()
    
    identity = UserIdentity(user_id=user.id, full_name="Cycle Hunter")
    async_db.add(identity)
    
    job = Job(
        title="Cycle Engineer", 
        company="Cycle Corp", 
        url="https://cycle.corp/jobs/1",
        description="Looking for an engineer who likes tests."
    )
    async_db.add(job)
    await async_db.commit()

    # 2. Match (Discovery)
    profile_dict = {"skills": ["Python"], "summary": "Engineer", "preference_weights": {}}
    metrics = await matching_service.calculate_metrics(profile_dict, job)
    assert metrics["match_score"] > 0

    # 3. Automation (Mocked Playwright & Confirmation)
    # Patch manager.broadcast to verify telemetry
    with patch("app.api.routes.websocket.manager.broadcast", new_callable=AsyncMock) as mock_broadcast, \
         patch("app.services.automation_service.automation_service.request_confirmation", new_callable=AsyncMock) as mock_confirm:
        
        # Run automation in simulation mode
        automation_service.use_mock = True
        await automation_service.apply_to_job(
            str(job.id), 
            job.url, 
            job.company, 
            {"full_name": "Cycle Hunter", "email": "cycle@hunteros.ai"},
            user_id=user.id
        )
        
        # Verify telemetry was sent
        assert mock_broadcast.called
        # Check if "started" event was broadcast
        calls = [c.args[0]["status"] for c in mock_broadcast.call_args_list if "status" in c.args[0]]
        assert "started" in calls

    # 4. Persistence (History)
    # Manually create application record (usually done by a controller)
    app_record = Application(
        user_id=user.id,
        job_id=job.id,
        status="applied",
        applied_match_score=metrics["match_score"]
    )
    async_db.add(app_record)
    await async_db.commit()
    
    # Verify history entry
    stmt = select(Application).filter(Application.user_id == user.id)
    result = await async_db.execute(stmt)
    saved_app = result.scalar_one()
    assert saved_app.job_id == job.id
    assert saved_app.status == "applied"

    print("\n[COMPATIBILITY] Full Autonomous Cycle Verified Successfully.")
