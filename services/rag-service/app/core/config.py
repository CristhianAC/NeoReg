from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user-service:8000"
    GOOGLE_API_KEY: str  


    class Config:
        env_file = ".env"

settings = Settings()