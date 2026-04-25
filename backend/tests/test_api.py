import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "online"

def test_security_headers():
    response = client.get("/")
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Strict-Transport-Security" in response.headers

def test_dashboard_stats_unauthorized():
    # Attempt to access protected route without token
    response = client.get("/api/v1/dashboard/stats")
    # Should be 401 Unauthorized or 403 Forbidden depending on implementation
    assert response.status_code in [401, 403]

def test_resume_download_unauthorized():
    # Attempt to access protected resume route without token
    response = client.get("/api/v1/resumes/sample.pdf")
    assert response.status_code in [401, 403]

def test_rate_limiting_config():
    # Verify that the limiter is attached to the app state
    assert hasattr(app.state, "limiter")
