from fastapi import FastAPI
from app.api.endpoints import rag



app = FastAPI(
    title="Employee RAG Service",
    description="Natural Language Query Service for Employee Data",
    version="1.0.0"
)



app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])