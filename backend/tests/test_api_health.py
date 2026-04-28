import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check_metrics():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "system" in data
    assert "cpu_usage_percent" in data["system"]
    assert "memory_usage_percent" in data["system"]
    assert "disk_usage_percent" in data["system"]
    
    # Values should be numbers
    assert isinstance(data["system"]["cpu_usage_percent"], (int, float))
    assert isinstance(data["system"]["memory_usage_percent"], (int, float))
