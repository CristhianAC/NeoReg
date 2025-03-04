from fastapi import FastAPI
from app.api.endpoints import rag
import openai
from app.core.config import settings

app = FastAPI(
    title="Employee RAG Service",
    description="Natural Language Query Service for Employee Data",
    version="1.0.0"
)

openai.api_key = settings.OPENAI_API_KEY

app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])