import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.automation_service import AutomationService, HumanBehavior

@pytest.mark.asyncio
async def test_human_behavior_jitter():
    # Verify jitter delay is a valid coroutine
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        await HumanBehavior.jitter_delay(100, 200)
        assert mock_sleep.called
        # Check if delay is within range (ms to seconds)
        args, _ = mock_sleep.call_args
        assert 0.1 <= args[0] <= 0.2

@pytest.mark.asyncio
async def test_fill_form_heuristics():
    # Mock playwright page and fields
    mock_page = AsyncMock()
    
    mock_field_first = AsyncMock()
    mock_field_first.get_attribute.side_effect = ["first_name_id", "First Name", "first_name", "text"]
    mock_field_first.is_visible.return_value = True
    
    mock_field_email = AsyncMock()
    mock_field_email.get_attribute.side_effect = ["email_id", "Email Address", "email", "email"]
    mock_field_email.is_visible.return_value = True
    
    mock_page.query_selector_all.return_value = [mock_field_first, mock_field_email]
    
    # Mock label query
    mock_label_first = AsyncMock()
    mock_label_first.inner_text.return_value = "First Name"
    
    mock_label_email = AsyncMock()
    mock_label_email.inner_text.return_value = "Email"
    
    # query_selector(label[for=...])
    mock_page.query_selector.side_effect = [mock_label_first, mock_label_email]
    
    # Mock screenshot return
    mock_page.screenshot.return_value = b"fake-screenshot"
    
    user_identity = {
        "full_name": "John Doe",
        "email": "john@example.com"
    }
    
    service = AutomationService(headless=True)
    # Patch jitter to avoid slow tests
    with patch("app.services.automation_service.HumanBehavior.jitter_delay", new_callable=AsyncMock):
        await service.fill_form(mock_page, user_identity)
    
    # Verify fill was called with correct data
    mock_field_first.fill.assert_any_call("John")
    mock_field_email.fill.assert_any_call("john@example.com")

@pytest.mark.asyncio
async def test_apply_to_job_high_risk_pause():
    service = AutomationService(headless=True)
    service.use_mock = True
    
    # User identity with high risk score
    user_identity = {
        "full_name": "John Doe",
        "job_risk_score": 85.0,
        "job_red_flags": ["Ghost Posting"]
    }
    
    with patch("app.services.automation_service.emit_agent_update", new_callable=AsyncMock) as mock_emit:
        with patch.object(service, "request_confirmation", new_callable=AsyncMock) as mock_confirm:
            await service.apply_to_job("job123", "http://test.com", "linkedin", user_identity)
            
            # Verify confirmation was requested due to high risk
            assert mock_confirm.called
            # Verify the risk warning was logged
            assert any("High-Risk Signal Detected" in call.args[2] for call in mock_emit.call_args_list)
