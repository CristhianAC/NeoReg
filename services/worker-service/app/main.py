from fastapi import FastAPI
from app.api.endpoints import worker

app = FastAPI(
    title="Worker Service API",
    description="API for managing worker-related operations",
    version="1.0.0"
)

app.include_router(worker.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Worker Service API"}