from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
import redis.asyncio as redis
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

import psutil

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    status = {
        "api": "online",
        "database": "offline",
        "redis": "offline",
        "worker": "offline"
    }
    
    # 1. Check DB
    try:
        await db.execute(text("SELECT 1"))
        status["database"] = "online"
    except Exception as e:
        logger.error(f"Health check DB error: {e}")
        
    # 2. Check Redis (Async)
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        if await r.ping():
            status["redis"] = "online"
        await r.close()
    except Exception as e:
        logger.error(f"Health check Redis error: {e}")
        
    # 3. Check Workers (Celery)
    try:
        from app.workers.celery_app import celery_app
        insp = celery_app.control.inspect()
        if insp and insp.ping():
            status["worker"] = "online"
    except Exception:
        pass
        
    # 4. Check AI Model
    try:
        from app.services.matching_service import matching_service
        # Small sanity check - embedding a single word
        test_embed = await matching_service.get_embeddings(["health"])
        if test_embed and len(test_embed) > 0:
            status["intelligence_engine"] = "online"
        else:
            status["intelligence_engine"] = "offline"
    except Exception as e:
        logger.error(f"Health check AI error: {e}")
        status["intelligence_engine"] = "error"
        
    # 5. System Metrics
    system_metrics = {
        "cpu_usage_percent": psutil.cpu_percent(),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent
    }
    
    # Overall Status
    is_healthy = status["api"] == "online" and status["database"] == "online"
    overall = "HEALTHY" if is_healthy else "DEGRADED"
    
    return {
        "status": overall,
        "details": status,
        "system": system_metrics,
        "resilience_pulse": "active",
        "version": "1.0.0"
    }
