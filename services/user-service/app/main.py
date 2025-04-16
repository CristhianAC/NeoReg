from fastapi import FastAPI
from app.api.endpoints import user, uploadPhoto, sql_executor, logs  # Add the new import
from app.utils.logger import logging_middleware  # Import the middleware

app = FastAPI(
    title="NeoReg API",
    description="API for NeoReg project",
    version="1.0.0"
)

# Add middleware
app.middleware("http")(logging_middleware)

app.include_router(user.router, prefix="/api/v1")
app.include_router(uploadPhoto.router, prefix="/api/v1")
app.include_router(sql_executor.router, prefix="/api/v1")
app.include_router(logs.router, prefix="/api/v1")  # Add the logs router

@app.get("/")
async def root():
    return {"message": "Welcome to NeoReg API"}