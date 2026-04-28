import pytest
import asyncio
from app.agents.execution_agent import ExecutionAgent

@pytest.mark.asyncio
async def test_execution_agent_navigation():
    """
    Verifies that ExecutionAgent can launch a browser and navigate to a URL.
    """
    agent = ExecutionAgent(user_id="test_user")
    try:
        await agent.start(headless=True)
        assert agent.page is not None
        
        # Navigate to a simple site
        await agent.navigate("https://example.com")
        
        # Verify content
        title = await agent.page.title()
        assert "Example Domain" in title
        
        content = await agent.page.content()
        assert "Example Domain" in content
        
    finally:
        await agent.stop()

@pytest.mark.asyncio
async def test_execution_agent_click_and_extract():
    """
    Verifies that ExecutionAgent can interact with the page.
    """
    agent = ExecutionAgent(user_id="test_user")
    try:
        await agent.start(headless=True)
        await agent.navigate("https://example.com")
        
        # Example.com has a link "More information..."
        await agent.page.click("a")
        
        # Wait for navigation
        await agent.page.wait_for_load_state("networkidle")
        
        new_url = agent.page.url
        assert "iana.org" in new_url
        
    finally:
        await agent.stop()
