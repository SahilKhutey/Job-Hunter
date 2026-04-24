from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import time

from app.core.config import settings
from app.core.database import get_db, engine, Base
from app.models.job import Job, Application
from app.models.profile import Profile
from app.services.matching_service import matching_service

from app.ai.llm_client import llm_client
from app.api.routes import user, automation, profile, application, agent, execution, websocket, jobs, dashboard, onboarding, resume, analytics

from fastapi.staticfiles import StaticFiles


from app.auth import routes as auth_routes
from app.auth import oauth_routes
from starlette.middleware.sessions import SessionMiddleware



# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Session Middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers FIRST
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
app.include_router(analytics.router, prefix="/api/v1", tags=["Dashboard Intelligence"])


# Mount static files for resume downloads
os.makedirs("static/resumes", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(websocket.router, tags=["WebSocket"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI Job Hunter OS API v1"}

@app.post("/api/v1/profile/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    parsed_data = parse_resume(content)
    profile = Profile(
        full_name=parsed_data.get("full_name", "Unknown"),
        email=parsed_data.get("email", ""),
        phone=parsed_data.get("phone", ""),
        raw_resume_text=parsed_data["raw_text"],
        skills=parsed_data["skills"],
        structured_data=parsed_data
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"id": profile.id, "status": "success", "data": parsed_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
