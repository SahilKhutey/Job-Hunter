import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.discovery_agent import DiscoveryAgent
from app.models.job import Job

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_execution_agent(mocker):
    # Mock ExecutionAgent inside DiscoveryAgent
    return mocker.patch("app.agents.discovery_agent.ExecutionAgent", autospec=True)

@pytest.mark.asyncio
async def test_discovery_agent_run(mock_db, mock_execution_agent):
    # Setup
    agent = DiscoveryAgent(user_id="test_user", db=mock_db)
    
    # Mock the browser interaction
    mock_browser_instance = mock_execution_agent.return_value
    mock_browser_instance.start = AsyncMock()
    mock_browser_instance.navigate = AsyncMock()
    mock_browser_instance.stop = AsyncMock()
    mock_browser_instance.page = MagicMock()
    
    # Mock URL extraction
    mock_browser_instance.page.evaluate = AsyncMock(return_value=["https://linkedin.com/jobs/1", "https://linkedin.com/jobs/2"])
    
    # Mock DB query
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    state = {"search_query": "Python Engineer", "search_location": "Remote"}
    
    # Run
    new_state = await agent.run(state)
    
    # Assert
    assert len(new_state["discovered_urls"]) == 2
    assert mock_db.add.call_count == 2
    mock_db.commit.assert_called_once()
    mock_browser_instance.stop.assert_called_once()
