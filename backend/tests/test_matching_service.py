import pytest
import numpy as np
from unittest.mock import MagicMock
from app.services.matching_service import MatchingEngine
from app.models.job import Job
from app.models.profile import Profile

@pytest.fixture
def mock_embedding_service(mocker):
    from unittest.mock import AsyncMock
    # Patch the method directly on the service instance used in the module
    mock_get = mocker.patch("app.services.matching_service.embedding_service.get_embedding", new_callable=AsyncMock)
    mock_get.return_value = np.array([1.0] * 384)
    return mock_get

@pytest.fixture
def matching_engine():
    return MatchingEngine()

@pytest.mark.asyncio
async def test_calculate_metrics_perfect_match(matching_engine, mock_embedding_service):
    # Setup profile and job with identical skills
    profile = Profile(
        skills=["Python", "FastAPI"],
        summary="Expert in Python and FastAPI",
        structured_data={"job_title": "Software Engineer"}
    )
    job = Job(
        title="Software Engineer",
        description="Looking for Python and FastAPI expert",
        skills_required=["Python", "FastAPI"]
    )
    
    # Mock embeddings
    mock_embedding_service.return_value = np.array([1.0] * 384)
    
    metrics = await matching_engine.calculate_metrics(profile, job)
    
    assert metrics["match_score"] >= 0.9  # High similarity expected
    assert metrics["priority"] == "HIGH"
    assert len(metrics["skill_gap"]) == 0

@pytest.mark.asyncio
async def test_calculate_metrics_with_risk(matching_engine, mock_embedding_service):
    profile = Profile(skills=["Python"])
    
    # Low risk job
    job_low_risk = Job(title="Safe Job", skills_required=["Python"], strategic_risk_score=0.0)
    # High risk job
    job_high_risk = Job(title="Risky Job", skills_required=["Python"], strategic_risk_score=80.0, red_flags=["Ghost Posting"])
    
    mock_embedding_service.return_value = np.array([1.0] * 384)
    
    metrics_low = await matching_engine.calculate_metrics(profile, job_low_risk)
    metrics_high = await matching_engine.calculate_metrics(profile, job_high_risk)
    
    assert metrics_high["match_score"] < metrics_low["match_score"]
    assert metrics_high["priority"] == "LOW"
    assert metrics_high["risk_assessment"]["score"] == 80.0

@pytest.mark.asyncio
async def test_calculate_metrics_no_match(matching_engine, mock_embedding_service):
    # Setup profile and job with disjoint skills
    profile = Profile(
        skills=["Java"],
        summary="Java developer",
        structured_data={"job_title": "Java Developer"}
    )
    job = Job(
        title="Frontend Dev",
        description="React and Vue developer",
        skills_required=["React", "Vue"]
    )
    
    # Mock disjoint embeddings (orthogonal vectors)
    mock_embedding_service.side_effect = [
        np.array([1.0] + [0.0] * 383), # user
        np.array([0.0] + [1.0] + [0.0] * 382) # job
    ]
    
    metrics = await matching_engine.calculate_metrics(profile, job)
    
    assert metrics["match_score"] < 0.4
    assert metrics["priority"] == "LOW"
    assert "react" in [s.lower() for s in metrics["skill_gap"]]

@pytest.mark.asyncio
async def test_match_jobs_sorting(matching_engine, mock_embedding_service):
    profile = Profile(skills=["Python"])
    job_good = Job(title="Good Job", skills_required=["Python"])
    job_bad = Job(title="Bad Job", skills_required=["C++"])
    
    # Mock embeddings to ensure 'Good Job' ranks higher
    mock_embedding_service.side_effect = [
        np.array([1.0] * 384), # user
        np.array([0.0] * 384), # job_bad
        np.array([1.0] * 384), # user (again for next call)
        np.array([1.0] * 384)  # job_good
    ]
    
    results = await matching_engine.match_jobs(profile, [job_bad, job_good])
    
    assert results[0][0].title == "Good Job"
    assert results[1][0].title == "Bad Job"
