from fastapi import FastAPI
from app.api.endpoints import rag, logs
from app.utils.logger import logging_middleware

app = FastAPI(
    title="Employee RAG Service",
    description="Natural Language Query Service for Employee Data",
    version="1.0.0"
)

# Add middleware
app.middleware("http")(logging_middleware)

app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
app.include_router(logs.router, prefix="/api/v1", tags=["logs"])