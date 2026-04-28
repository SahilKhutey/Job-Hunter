import pytest
import json
from unittest.mock import AsyncMock
from app.services.resume_ai import parse_resume_to_json

@pytest.fixture
def mock_llm_client(mocker):
    # Patch the llm_client instance used in app.services.resume_ai
    mock = AsyncMock()
    mocker.patch("app.services.resume_ai.llm_client", mock)
    return mock

@pytest.mark.asyncio
async def test_parse_resume_to_json_success(mock_llm_client):
    # Mock LLM response
    mock_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "SQL"]
    }
    mock_llm_client.chat_completion.return_value = f"```json\n{json.dumps(mock_data)}\n```"
    
    result = await parse_resume_to_json("Raw resume text")
    
    assert result["full_name"] == "John Doe"
    assert "Python" in result["skills"]
    mock_llm_client.chat_completion.assert_called_once()

@pytest.mark.asyncio
async def test_parse_resume_to_json_fallback(mock_llm_client):
    # Mock LLM failure
    mock_llm_client.chat_completion.side_effect = Exception("API Error")
    
    result = await parse_resume_to_json("Raw resume text")
    
    assert result["full_name"] == ""
    assert result["skills"] == []
