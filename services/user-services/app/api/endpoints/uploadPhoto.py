from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Not found"}}
)

@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    if file.size > 2 * 1024 * 1024:  # 2 MB
        raise HTTPException(status_code=400, detail="Archivo demasiado grande")
    return {"filename": file.filename}