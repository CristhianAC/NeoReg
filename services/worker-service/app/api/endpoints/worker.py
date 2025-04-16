from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import PersonalDataDB
from app.models.schemas import PersonalDataResponse
from app.utils.logger import APILogger
import uuid

router = APIRouter()

@router.get("/workers/", response_model=List[PersonalDataResponse])
async def get_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    try:
        workers = db.query(PersonalDataDB).offset(skip).limit(limit).all()
        return workers
    except Exception as e:
        error_msg = f"Error retrieving workers: {str(e)}"
        APILogger.log_error(request_id, error_msg, 500)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/workers/{worker_id}", response_model=PersonalDataResponse)
async def get_worker(worker_id: int, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    
    worker = db.query(PersonalDataDB).filter(PersonalDataDB.id == worker_id).first()
    if worker is None:
        error_msg = f"Worker with id {worker_id} not found"
        APILogger.log_error(request_id, error_msg, 404)
        raise HTTPException(status_code=404, detail=error_msg)
    return worker