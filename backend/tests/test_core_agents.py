import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.resume_agent import ResumeAgent
from app.agents.matching_agent import MatchingAgent

@pytest.mark.asyncio
async def test_matching_agent_run():
    agent = MatchingAgent()
    state = {
        "job": {"description": "Looking for a Python developer with FastAPI experience."},
        "profile": {"skills": ["Python", "FastAPI", "React"], "summary": "Senior Dev"}
    }
    
    # MatchingEngine returns a dict
    mock_metrics = {
        "match_score": 0.85,
        "matched_skills": ["Python", "FastAPI"],
        "skill_gap": [],
        "difficulty": 0.4,
        "priority": "MEDIUM"
    }
    
    with patch("app.services.matching_service.matching_service.calculate_metrics", return_value=mock_metrics):
        new_state = await agent.run(state)
        assert new_state["match_score"] == 0.85
        assert "FastAPI" in new_state["match_analytics"]["matched_skills"]

@pytest.mark.asyncio
async def test_resume_agent_run_success():
    agent = ResumeAgent()
    state = {
        "profile": {"full_name": "Test User"},
        "job": {"description": "Job desc", "id": 123},
        "user_id": "456"
    }
    
    mock_tailored_resume = {"summary": "Tailored summary", "skills": ["Python"]}
    
    with patch("app.services.resume_tailor.resume_tailor.generate_tailored_resume", new_callable=AsyncMock) as mock_tailor:
        with patch("app.utils.pdf_generator.pdf_generator.generate_resume", return_value="/tmp/test.pdf") as mock_pdf:
            mock_tailor.return_value = mock_tailored_resume
            
            new_state = await agent.run(state)
            
            assert new_state["resume_json"]["summary"] == "Tailored summary"
            assert new_state["resume_pdf_path"] == "/tmp/test.pdf"
            mock_pdf.assert_called_once()

@pytest.mark.asyncio
async def test_resume_agent_missing_data():
    agent = ResumeAgent()
    state = {} # Missing profile/job
    
    new_state = await agent.run(state)
    assert "resume_json" not in new_state
