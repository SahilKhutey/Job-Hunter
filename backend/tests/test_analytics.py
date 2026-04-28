import pytest
from app.services.analytics_service import analytics_service
from unittest.mock import MagicMock

def test_compute_dashboard_stats():
    # Mock applications
    app1 = MagicMock(status="applied")
    app2 = MagicMock(status="interview")
    app3 = MagicMock(status="rejected")
    app4 = MagicMock(status="offer")
    
    # Mock jobs with and without risk
    job1 = MagicMock(strategic_risk_score=75) # High risk
    job2 = MagicMock(strategic_risk_score=20) # Low risk
    job3 = MagicMock(strategic_risk_score=90) # High risk
    
    apps = [app1, app2, app3, app4]
    jobs = [job1, job2, job3]
    
    stats = analytics_service.compute_dashboard_stats(apps, jobs)
    
    assert stats["total_applications"] == 4
    assert stats["interview_rate"] == 25.0
    assert stats["active_applications"] == 2 
    assert stats["risks_avoided"] == 2 # job1 and job3
    assert stats["status_breakdown"]["applied"] == 1
    assert stats["status_breakdown"]["interview"] == 1

def test_analyze_resume_performance():
    app1 = MagicMock(status="interview", resume_version="v1")
    app2 = MagicMock(status="applied", resume_version="v1")
    app3 = MagicMock(status="interview", resume_version="v2")
    
    perf = analytics_service.analyze_resume_performance([app1, app2, app3])
    
    assert perf["v1"]["total"] == 2
    assert perf["v1"]["interviews"] == 1
    assert perf["v1"]["rate"] == 50.0
    
    assert perf["v2"]["total"] == 1
    assert perf["v2"]["interviews"] == 1
    assert perf["v2"]["rate"] == 100.0

def test_analyze_score_correlation():
    app1 = MagicMock(status="interview", applied_match_score=0.92)
    app2 = MagicMock(status="applied", applied_match_score=0.85)
    app3 = MagicMock(status="rejected", applied_match_score=0.70)
    app4 = MagicMock(status="interview", applied_match_score=0.95)
    
    corr = analytics_service.analyze_score_correlation([app1, app2, app3, app4])
    
    assert corr["90-100"]["volume"] == 2
    assert corr["90-100"]["rate"] == 100.0
    assert corr["80-89"]["volume"] == 1
    assert corr["80-89"]["rate"] == 0.0

def test_generate_ai_insights():
    stats = {"interview_rate": 5, "total_applications": 20}
    resume_perf = {"v1": {"rate": 10}, "v2": {"rate": 40}}
    platform_perf = {"LinkedIn": {"rate": 30}}
    # Bucketed correlation
    score_corr = {
        "90-100": {"rate": 85.0, "volume": 5},
        "80-89": {"rate": 20.0, "volume": 10}
    }
    
    insights = analytics_service.generate_ai_insights(stats, resume_perf, platform_perf, score_corr)
    
    messages = [i["message"] for i in insights]
    
    # Low interview rate warning
    assert any("Low conversion rate" in m for m in messages)
    # Best resume insight
    assert any("version 'v2' is outperforming" in m for m in messages)
    # Correlation insight
    assert any("Strong correlation" in m for m in messages)
