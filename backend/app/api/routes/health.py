from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
import redis
import os
from app.workers.celery_app import celery_app

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    status = {
        "api": "online",
        "database": "offline",
        "redis": "offline",
        "worker": "offline"
    }
    
    # 1. Check DB
    try:
        db.execute("SELECT 1")
        status["database"] = "online"
    except Exception:
        pass
        
    # 2. Check Redis
    try:
        r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        if r.ping():
            status["redis"] = "online"
    except Exception:
        pass
        
    # 4. Check Browser Engine (Integrity)
    try:
        from app.automation.stealth import stealth_config
        status["browser_engine"] = "online"
    except Exception:
        status["browser_engine"] = "offline"
        
    # Overall Status
    overall = "HEALTHY" if all(v == "online" for v in status.values()) else "DEGRADED"
    
    return {
        "status": overall,
        "details": status,
        "resilience_pulse": "active",
        "last_recovery": "none"
    }
