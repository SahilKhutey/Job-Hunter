import pytest
import asyncio
from app.execution.engine import run_application
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_run_application_flow(mocker):
    """
    Verifies the full async run_application flow with mocked Playwright and Adapters.
    """
    # Mock data
    job = {"id": 123, "url": "https://example.com/job"}
    profile = {"full_name": "Test User", "email": "test@example.com"}
    user_id = 1
    
    # Mock log_application
    mock_log = mocker.patch("app.execution.engine.log_application")
    
    # Mock get_adapter
    mock_adapter = AsyncMock()
    mocker.patch("app.execution.engine.get_adapter", return_value=mock_adapter)
    
    # Mock Playwright
    mock_p = AsyncMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    # Setup chain: p.chromium.launch -> browser.new_context -> context.new_page
    mock_p.chromium.launch.return_value = mock_browser
    mocker.patch("app.execution.engine.load_session", return_value=mock_context)
    mock_context.new_page.return_value = mock_page
    
    with patch("app.execution.engine.async_playwright") as mock_ap:
        # async_playwright() returns a context manager that enters and returns mock_p
        mock_ap.return_value.__aenter__.return_value = mock_p
        
        result = await run_application(user_id, job, profile)
        
    # Verify calls
    assert result["status"] == "completed"
    
    # Verify adapter calls (awaitable)
    mock_adapter.open_job.assert_called_once_with(mock_page, job)
    mock_adapter.click_apply.assert_called_once_with(mock_page)
    mock_adapter.fill_form.assert_called_once_with(mock_page, profile)
    mock_adapter.submit.assert_called_once_with(mock_page)
    
    # Verify log calls
    assert mock_log.call_count >= 2 # started, awaiting_confirmation, submitted
    
@pytest.mark.asyncio
async def test_run_application_failure(mocker):
    """
    Verifies error handling in run_application.
    """
    job = {"id": 123, "url": "https://example.com/job"}
    profile = {}
    user_id = 1
    
    mock_log = mocker.patch("app.execution.engine.log_application")
    mocker.patch("app.execution.engine.get_adapter", side_effect=Exception("Adapter crash"))
    
    with patch("app.execution.engine.async_playwright") as mock_ap:
        with pytest.raises(Exception) as exc:
            await run_application(user_id, job, profile)
            
    assert "Adapter crash" in str(exc.value)
    mock_log.assert_any_call(user_id, 123, "failed")
