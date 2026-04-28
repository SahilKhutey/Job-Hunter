from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Request
print("--- STARTING HUNTEROS API ---")
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import time
import os
import json

from app.core.config import settings
from app.core.database import get_db, engine, Base
from app.models.job import Job, Application
from app.models.profile import Profile
from app.services.matching_service import matching_service

from app.ai.llm_client import llm_client
from app.api.routes import user, automation, profile, application, agent, execution, websocket, jobs, dashboard, onboarding, resume, analytics, health, interview, extension

from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
# import sentry_sdk

from app.auth import routes as auth_routes
from app.auth import oauth_routes
from starlette.middleware.sessions import SessionMiddleware

# Database initialization (Using a temporary sync engine for schema creation)
from sqlalchemy import create_engine
sync_url = settings.DATABASE_URL
sync_engine = create_engine(sync_url)
Base.metadata.create_all(bind=sync_engine)

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
from contextlib import asynccontextmanager
from app.services.monitor import monitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("--- HunterOS Resilience Engine: Starting ---")
    monitor.start()
    yield
    # Shutdown logic
    print("--- HunterOS Resilience Engine: Shutting Down ---")
    await monitor.stop()

app = FastAPI(
    title="HunterOS API",
    description="Autonomous Career Execution Engine",
    version="1.0.0",
    lifespan=lifespan
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global Resilience Handler ────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    from app.api.routes.websocket import emit_agent_update
    
    logger = logging.getLogger("app.main")
    logger.error(f"UNHANDLED_EXCEPTION: {str(exc)}", exc_info=True)
    
    # Alert Mission Control
    try:
        await emit_agent_update(
            agent="System", 
            status="error", 
            message=f"Critical Internal Error: {str(exc)[:100]}..."
        )
    except Exception:
        pass
        
    return HTTPException(status_code=500, detail="Internal Server Error").__dict__


# Add Session Middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

from app.auth.dependencies import get_current_user

# Security: Protected static files route
@app.get("/api/v1/resumes/{filename}")
async def get_protected_resume(filename: str, current_user = Depends(get_current_user)):
    file_path = os.path.join("static", "resumes", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)

from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        
        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' ws: wss:;"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(SecurityHeadersMiddleware)



# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["System"])
app.include_router(websocket.router, tags=["WebSocket"])
app.include_router(auth_routes.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(oauth_routes.router, prefix="/api/v1/auth", tags=["OAuth"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User Identity"])

app.include_router(onboarding.router, prefix="/api/v1", tags=["Onboarding"])
app.include_router(resume.router, prefix="/api/v1", tags=["Resume Optimization"])
app.include_router(automation.router, prefix="/api/v1/automation", tags=["Automation Copilot"])

app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile Intelligence"])
app.include_router(application.router, prefix="/api/v1/application", tags=["Application Generation"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["Multi-Agent Pipeline"])
app.include_router(execution.router, prefix="/api/v1/execution", tags=["Application Execution Engine"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Job Feed"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard Intelligence"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(interview.router, prefix="/api/v1/interview", tags=["Interview Simulation"])
app.include_router(extension.router, prefix="/api/v1/extension", tags=["Browser Extension"])

# Instrumentation
Instrumentator().instrument(app).expose(app)

@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"status": "online", "message": "HunterOS Secure API v1"}




if __name__ == "__main__":
    print("--- ENTERING MAIN BLOCK ---")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
