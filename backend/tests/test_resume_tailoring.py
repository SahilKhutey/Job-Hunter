import pytest
import json
from unittest.mock import AsyncMock
from app.services.resume_tailor import resume_tailor

@pytest.fixture
def mock_llm_client(mocker):
    mock = AsyncMock()
    mocker.patch("app.services.resume_tailor.llm_client", mock)
    return mock

@pytest.mark.asyncio
async def test_generate_tailored_resume_success(mock_llm_client):
    profile = {"skills": ["Python"]}
    job_desc = "Looking for a Python expert."
    
    mock_data = {
        "summary": "Expert Python developer.",
        "skills": ["Python", "Backend"],
        "experience": [],
        "projects": [],
        "education": "CS Degree"
    }
    mock_llm_client.chat_completion.return_value = json.dumps(mock_data)
    
    result = await resume_tailor.generate_tailored_resume(profile, job_desc)
    
    assert result["summary"] == "Expert Python developer."
    assert "Backend" in result["skills"]
    assert mock_llm_client.chat_completion.called

@pytest.mark.asyncio
async def test_generate_tailored_resume_fallback(mock_llm_client):
    profile = {"skills": ["Python"], "summary": "Old summary"}
    job_desc = "Looking for a Python expert."
    
    mock_llm_client.chat_completion.side_effect = Exception("LLM Error")
    
    result = await resume_tailor.generate_tailored_resume(profile, job_desc)
    
    assert result["summary"] == "Old summary"
    assert result["skills"] == ["Python"]

def test_verify_authenticity_valid():
    original = {"experience": [{"company": "Google"}]}
    tailored = {"experience": [{"company": "Google"}]}
    assert resume_tailor.verify_authenticity(original, tailored) is True

def test_verify_authenticity_hallucination():
    original = {"experience": [{"company": "Google"}]}
    tailored = {"experience": [{"company": "Google"}, {"company": "SpaceX"}]}
    # SpaceX was not in original
    assert resume_tailor.verify_authenticity(original, tailored) is False

@pytest.mark.asyncio
async def test_hallucination_warning_triggered(mock_llm_client, caplog):
    profile = {"experience": [{"company": "Google"}]}
    job_desc = "Job at SpaceX."
    
    # AI Hallucinates SpaceX as a past job
    mock_data = {
        "summary": "Expert",
        "skills": [],
        "experience": [{"company": "Google"}, {"company": "SpaceX"}],
        "projects": [],
        "education": "CS"
    }
    mock_llm_client.chat_completion.return_value = json.dumps(mock_data)
    
    await resume_tailor.generate_tailored_resume(profile, job_desc)
    
    assert "Hallucination detected" in caplog.text
