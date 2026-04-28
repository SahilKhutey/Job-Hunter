from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Job Hunter OS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    REDIS_URL: str
    OPENAI_API_KEY: str
    
    SECRET_KEY: str # Unifying with dependencies.py
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 # 15 minutes for Zero-Trust
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    SENTRY_DSN: Optional[str] = None


    # OAuth Settings (Optional)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None

    model_config = ConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
