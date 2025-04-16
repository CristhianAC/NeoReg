from fastapi import FastAPI
from app.api.endpoints import worker, logs
from app.utils.logger import logging_middleware

app = FastAPI(
    title="Worker Service API",
    description="API for managing worker-related operations",
    version="1.0.0"
)

# Add middleware
app.middleware("http")(logging_middleware)

app.include_router(worker.router, prefix="/api/v1")
app.include_router(logs.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Worker Service API"}