from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/personas/")
async def create_persona(
    persona: schemas.PersonalData,
    db: Session = Depends(get_db)
):
   
    db_persona = persona.to_db_model()
    
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    
    return {"id": db_persona.id}