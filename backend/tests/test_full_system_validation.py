import pytest
import json
from unittest.mock import MagicMock, AsyncMock
from app.services.analytics_service import analytics_service
from app.services.resume_tailor import resume_tailor
from app.services.interview_service import interview_service
from app.services.negotiation_service import negotiation_service

@pytest.mark.asyncio
async def test_full_strategic_cycle_validation(mocker):
    """
    Validates the end-to-end strategic intelligence flow:
    Risk Detection -> Analytics -> Tailoring -> Interview -> Negotiation
    """
    
    # 1. MOCK DATA
    profile = {
        "summary": "Expert Developer",
        "skills": ["Python", "AWS"],
        "experience": [{"company": "Google", "role": "Senior dev"}]
    }
    
    high_risk_job = {
        "id": 101,
        "title": "Staff Engineer",
        "company": "Volatility Inc",
        "description": "Fast paced environment...",
        "strategic_risk_score": 85,
        "red_flags": ["High leadership churn", "Negative financial outlook"]
    }
    
    # 2. ANALYTICS VALIDATION (Risk Avoidance)
    stats = analytics_service.compute_dashboard_stats([], [high_risk_job])
    assert stats["risks_avoided"] == 1
    
    # 3. TAILORING VALIDATION (Veracity)
    mock_llm = AsyncMock()
    mocker.patch("app.services.resume_tailor.llm_client", mock_llm)
    mock_logger = mocker.patch("app.services.resume_tailor.logger")
    
    # Mock AI trying to hallucinate
    mock_llm.chat_completion.return_value = json.dumps({
        "summary": "Expert", "skills": ["Python"],
        "experience": [{"company": "Google"}, {"company": "Volatility Inc"}],
        "projects": [], "education": "CS"
    })
    
    await resume_tailor.generate_tailored_resume(profile, "Job Desc")
    # Check if warning was called with hallucination message
    assert mock_logger.warning.called
    warning_msg = mock_logger.warning.call_args[0][0]
    assert "Hallucination detected" in warning_msg

    # 4. INTERVIEW VALIDATION (Strategic Prep)
    mocker.patch("app.services.interview_service.llm_client", mock_llm)
    mock_llm.generate_structured_json.return_value = [
        {"id": 1, "question": "Explain churn?", "type": "strategic"}
    ]
    
    questions = await interview_service.generate_questions(high_risk_job, profile)
    assert questions[0]["type"] == "strategic"
    
    # 5. NEGOTIATION VALIDATION (Risk Premium)
    mocker.patch("app.services.negotiation_service.llm_client", mock_llm)
    mock_llm.generate_text.return_value = json.dumps({
        "offer_grade": 60,
        "leverage_points": ["Risk Premium for Volatility"],
        "strategy": "Aggressive",
        "counter_script": "Template"
    })
    
    neg_strategy = await negotiation_service.generate_strategy(
        {"base_salary": "100k", "equity": "0", "bonus": "0"},
        high_risk_job,
        profile
    )
    assert "Risk Premium" in neg_strategy["leverage_points"][0]

    print("\n[SUCCESS] FULL SYSTEM STRATEGIC VALIDATION PASSED")
