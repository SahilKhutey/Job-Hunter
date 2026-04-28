import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.learning_agent import LearningAgent

@pytest.mark.asyncio
async def test_learning_agent_reinforcement():
    agent = LearningAgent()
    
    mock_db = AsyncMock()
    mock_profile = MagicMock()
    # New Elite weights schema
    mock_profile.preference_weights = {
        "skills": 1.0, "experience": 1.0, "education": 1.0, 
        "location": 1.0, "company_tier": 1.0, "industry_relevance": 1.0
    }
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_profile
    mock_db.execute.return_value = mock_result
    
    state = {
        "profile_id": 1,
        "feedback": "interview_success"
    }
    
    await agent.run(state, db=mock_db)
    
    # Verify reinforcement (1.0 * 1.10 = 1.10)
    assert mock_profile.preference_weights["skills"] == pytest.approx(1.10)
    assert mock_profile.preference_weights["experience"] == pytest.approx(1.05)
    assert mock_profile.preference_weights["industry_relevance"] == pytest.approx(1.10)

@pytest.mark.asyncio
async def test_learning_agent_penalty():
    agent = LearningAgent()
    
    mock_db = AsyncMock()
    mock_profile = MagicMock()
    mock_profile.preference_weights = {
        "skills": 1.0, "experience": 1.0, "education": 1.0, 
        "location": 1.0, "company_tier": 1.0, "industry_relevance": 1.0
    }
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_profile
    mock_db.execute.return_value = mock_result
    
    state = {
        "profile_id": 1,
        "feedback": "match_rejected",
        "rejection_reason": "location"
    }
    
    await agent.run(state, db=mock_db)
    
    # Verify penalty (1.0 * 0.85 = 0.85)
    assert mock_profile.preference_weights["location"] == pytest.approx(0.85)
    assert mock_profile.preference_weights["skills"] == 1.0 # Unchanged
