import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, MagicMock
from app.auth.dependencies import get_current_user
from app.core.database import get_db

from datetime import datetime

@pytest.mark.asyncio
async def test_dashboard_stats_api(mocker):
    # Mock dependencies
    mock_user = MagicMock()
    mock_user.id = 1
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_db = AsyncMock()
    # Mock return for count queries and applications select
    mock_count_result = MagicMock()
    mock_count_result.scalar.return_value = 10
    
    mock_apps_result = MagicMock()
    mock_app = MagicMock()
    mock_app.status = "applied"
    mock_apps_result.scalars.return_value.all.return_value = [mock_app]
    
    mock_db.execute.side_effect = [mock_count_result, mock_apps_result, mock_count_result, mock_count_result]
    
    # Mock analytics service to avoid real computation on mocks
    mocker.patch("app.api.routes.dashboard.analytics_service.compute_dashboard_stats", return_value={
        "total_applications": 1,
        "interview_rate": 0.5,
        "status_breakdown": {}
    })
    mocker.patch("app.api.routes.dashboard.analytics_service.analyze_resume_performance", return_value={})
    mocker.patch("app.api.routes.dashboard.analytics_service.analyze_platform_performance", return_value={})
    mocker.patch("app.api.routes.dashboard.analytics_service.generate_ai_insights", return_value=[])
    
    app.dependency_overrides[get_db] = lambda: mock_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/dashboard/stats?profile_id=1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs_analyzed"] == 10
    
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_dashboard_activity_api(mocker):
    mock_user = MagicMock()
    mock_user.id = 1
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_db = AsyncMock()
    mock_result = MagicMock()
    
    # Mock activity data
    mock_activity = MagicMock()
    mock_activity.id = 1
    mock_activity.status = "APPLIED"
    mock_activity.applied_at = datetime(2026, 4, 28)
    mock_activity.job = MagicMock()
    mock_activity.job.company = "Test Co"
    mock_activity.job.title = "Software Engineer"
    
    # Mock for Job Match query
    mock_job = MagicMock()
    mock_job.company = "Match Co"
    mock_job.title = "AI Engineer"
    mock_job.match_score = 0.95
    mock_job.posted_at = datetime(2026, 4, 28)
    mock_job.ai_decision = "AUTO_APPLY_READY"

    mock_scalars_apps = MagicMock()
    mock_scalars_apps.all.return_value = [mock_activity]
    
    mock_scalars_jobs = MagicMock()
    mock_scalars_jobs.all.return_value = [mock_job]
    
    mock_result_apps = MagicMock()
    mock_result_apps.scalars.return_value = mock_scalars_apps
    
    mock_result_jobs = MagicMock()
    mock_result_jobs.scalars.return_value = mock_scalars_jobs
    
    mock_db.execute.side_effect = [mock_result_apps, mock_result_jobs]
    
    app.dependency_overrides[get_db] = lambda: mock_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/dashboard/activity?profile_id=1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Check if at least one entry matches
    found = any(d["title"] == "Application submitted to Test Co" for d in data)
    assert found
    
    app.dependency_overrides = {}
