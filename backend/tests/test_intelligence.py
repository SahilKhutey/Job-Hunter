import pytest
import asyncio
from app.services.intelligence_engine import user_intelligence_engine

@pytest.mark.asyncio
async def test_red_flag_detection_burnout():
    """Verify that burnout culture keywords are correctly flagged."""
    jd = "We are a high-growth startup looking for rockstars who are comfortable with 24/7 availability and a work hard play hard culture."
    analysis = await user_intelligence_engine.analyze_red_flags(jd)
    
    assert "Burnout Culture" in analysis["flags"]
    assert analysis["risk_score"] >= 25

@pytest.mark.asyncio
async def test_red_flag_detection_instability():
    """Verify that instability indicators are correctly flagged."""
    jd = "Urgent backfill needed for a vacancy. Immediate hire."
    analysis = await user_intelligence_engine.analyze_red_flags(jd)
    
    assert "Organizational Instability" in analysis["flags"]
    assert analysis["risk_score"] >= 25

@pytest.mark.asyncio
async def test_red_flag_detection_ambiguity():
    """Verify that vague expectations are correctly flagged."""
    jd = "You will wear many hats and handle various tasks as needed. Competitive salary."
    analysis = await user_intelligence_engine.analyze_red_flags(jd)
    
    assert "Expectation Ambiguity" in analysis["flags"]
    assert analysis["risk_score"] >= 25

@pytest.mark.asyncio
async def test_combined_risk_score():
    """Verify that multiple flags increase the risk score appropriately."""
    jd = "High-growth startup with 24/7 availability. Immediate hire for backfill. Wear many hats."
    analysis = await user_intelligence_engine.analyze_red_flags(jd)
    
    assert len(analysis["flags"]) >= 3
    assert analysis["risk_score"] >= 75
