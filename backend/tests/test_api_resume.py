import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, MagicMock, patch
from app.auth.dependencies import get_current_user
from app.core.database import get_db

@pytest.mark.asyncio
async def test_tailor_resume_api(mocker):
    # Mock dependencies
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    
    mock_profile = MagicMock()
    mock_profile.id = 1
    mock_profile.email = "test@example.com"
    mock_profile.summary = "Old summary"
    mock_profile.skills = ["Python"]
    mock_profile.structured_data = {"experience": [], "education": [], "job_title": "Dev"}
    
    # Overrides
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_db_session = AsyncMock()
    # Mock db.execute(stmt) -> result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.side_effect = [None, mock_profile] # None for identity, mock_profile for profile
    mock_db_session.execute.return_value = mock_result
    
    app.dependency_overrides[get_db] = lambda: mock_db_session

    # Mock internal services
    mock_tailor = AsyncMock(return_value={"summary": "Tailored summary", "skills": ["Python", "AI"]})
    mocker.patch("app.api.routes.resume.tailor_resume", mock_tailor)
    mocker.patch("app.api.routes.resume.generate_resume_pdf", return_value="static/resumes/test.pdf")
    
    # Correct AsyncClient usage for modern httpx
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/resume/tailor", json={"job_description": "Need AI Expert"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["resume"]["summary"] == "Tailored summary"
    
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_score_resume_api(mocker):
    mock_user = MagicMock()
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    mock_score = AsyncMock(return_value={"final_score": 85, "feedback": {}})
    mocker.patch("app.api.routes.resume.score_resume", mock_score)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/resume/score", json={
            "resume_text": "My resume",
            "job_description": "The job"
        })
    
    assert response.status_code == 200
    assert response.json()["final_score"] == 85
    
    app.dependency_overrides = {}
