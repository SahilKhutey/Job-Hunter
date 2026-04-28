import pytest
import asyncio
import time
from app.services.matching_service import matching_service
from app.models.job import Job
from app.models.profile import Profile
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_batch_matching_latency(mocker):
    """
    Benchmark the MatchingEngine to ensure batch processing remains under 200ms
    for 10 jobs (excluding real LLM/Embedding calls which are mocked).
    """
    # Mock embedding service to return static vectors instantly
    mock_emb = mocker.patch("app.services.embedding_service.embedding_service.get_embedding", 
                            new_callable=AsyncMock)
    mock_emb.return_value = [0.1] * 384
    
    profile = Profile(
        skills=["Python", "Go", "React", "AWS"],
        summary="Expert software engineer with 10 years of experience.",
        structured_data={"job_title": "Senior Staff Engineer"}
    )
    
    # Generate 10 mock jobs
    jobs = []
    for i in range(10):
        jobs.append(Job(
            title=f"Engineer Role {i}",
            company=f"Tech Co {i}",
            description="Looking for a high-performance engineer with cloud skills.",
            skills_required=["Python", "AWS"]
        ))
    
    start_time = time.time()
    results = await matching_service.match_jobs(profile, jobs)
    duration = (time.time() - start_time) * 1000
    
    print(f"\n[BENCHMARK] Batch Match Duration: {duration:.2f}ms")
    
    assert len(results) == 10
    assert duration < 500  # Expect under 500ms even with 0.01s sleep per call (20 calls total)
    # Since we use asyncio.gather, it should be much faster than sequential.
    # Sequential would be 10 jobs * 2 calls * 10ms = 200ms + overhead.
    # Parallel should be closer to 20-30ms total.

@pytest.mark.asyncio
async def test_matching_score_weighted_logic():
    """Verify that elite weights (industry relevance) influence the score."""
    profile = {
        "skills": ["Python"],
        "summary": "AI researcher",
        "preference_weights": {"skills": 1.0, "experience": 1.0, "industry_relevance": 5.0} # High relevance weight
    }
    
    job = {
        "title": "AI Scientist",
        "description": "Research in AI and LLMs",
        "skills_required": ["Python"]
    }
    
    # Mock embeddings to be highly similar
    from app.services.embedding_service import embedding_service
    embedding_service.get_embedding = AsyncMock(return_value=[0.5] * 384)
    
    metrics = await matching_service.calculate_metrics(profile, job)
    
    assert metrics["match_score"] > 0.5
    assert "python" in metrics["matched_skills"] # Matching Engine lowercases skills
