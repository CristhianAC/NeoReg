from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    USER_SERVICE_URL: str = "http://user-service:8000"  # Default for Docker environment
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }

settings = Settings()