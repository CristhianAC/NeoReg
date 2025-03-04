from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user-service:8000"
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-2.0-flash"
    VECTOR_DB_HOST: str = "vector-db"
    VECTOR_DB_PORT: int = 6333

    class Config:
        env_file = ".env"

settings = Settings()