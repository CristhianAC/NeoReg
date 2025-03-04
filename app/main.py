from fastapi import FastAPI
from api.endpoints import user, uploadPhoto # Importar los routers

app = FastAPI(
    title="NeoReg API",
    description="API for NeoReg project",
    version="1.0.0"
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(uploadPhoto.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to NeoReg API"}