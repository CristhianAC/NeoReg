from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import PersonalDataDB
from app.models.schemas import PersonalDataResponse

router = APIRouter()

@router.get("/workers/", response_model=List[PersonalDataResponse])
async def get_workers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workers = db.query(PersonalDataDB).offset(skip).limit(limit).all()
    return workers

@router.get("/workers/{worker_id}", response_model=PersonalDataResponse)
async def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(PersonalDataDB).filter(PersonalDataDB.id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker