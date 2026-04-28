import pytest
from unittest.mock import AsyncMock, patch
from app.services.negotiation_service import negotiation_service

@pytest.mark.asyncio
async def test_generate_strategy_success():
    offer = {
        "base_salary": "$150,000",
        "equity": "0.1%",
        "bonus": "$20,000"
    }
    job_details = {
        "title": "Senior Software Engineer",
        "company": "TechCorp"
    }
    profile = {
        "summary": "Experienced backend dev",
        "skills": ["Python", "AWS", "FastAPI"]
    }

    # Mock the LLM call to return a specific JSON
    mock_llm_response = """
    {
        "offer_grade": 85,
        "leverage_points": ["Deep Python expertise", "Current equity is below market", "Proven track record"],
        "strategy": "Push for 10% more base and 0.05% more equity.",
        "counter_script": "Dear Manager, thank you for the offer..."
    }
    """
    
    with patch("app.ai.llm_client.llm_client.generate_text", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = mock_llm_response
        
        result = await negotiation_service.generate_strategy(offer, job_details, profile)
        
        assert result["offer_grade"] == 85
        assert len(result["leverage_points"]) == 3
        assert "Push for 10% more" in result["strategy"]
        assert "Dear Manager" in result["counter_script"]
        mock_generate.assert_called_once()

@pytest.mark.asyncio
async def test_generate_strategy_fallback():
    # Test fallback when LLM fails
    offer = {"base_salary": "$100k"}
    job_details = {"title": "Dev"}
    profile = {"skills": ["C++"]}
    
    with patch("app.ai.llm_client.llm_client.generate_text", new_callable=AsyncMock) as mock_generate:
        mock_generate.side_effect = Exception("LLM Error")
        
        result = await negotiation_service.generate_strategy(offer, job_details, profile)
        
        # Should return fallback values
        assert result["offer_grade"] == 75
        assert "leverage_points" in result
        assert "strategy" in result
        assert "counter_script" in result
