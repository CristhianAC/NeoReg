from fastapi import FastAPI
from app.api.endpoints import user, uploadPhoto, sql_executor  # Add the new import

app = FastAPI(
    title="NeoReg API",
    description="API for NeoReg project",
    version="1.0.0"
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(uploadPhoto.router, prefix="/api/v1")
app.include_router(sql_executor.router, prefix="/api/v1")  # Add the new router

@app.get("/")
async def root():
    return {"message": "Welcome to NeoReg API"}