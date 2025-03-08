from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import PersonalDataDB
from app.models.schemas import PersonalData, PersonalDataResponse

router = APIRouter()

@router.post("/personas/", response_model=PersonalDataResponse)
async def create_persona(persona: PersonalData, db: Session = Depends(get_db)):
    db_persona = PersonalDataDB(
        primer_nombre=persona.primer_nombre,
        segundo_nombre=persona.segundo_nombre,
        apellidos=persona.apellidos,
        fecha_nacimiento=persona.fecha_nacimiento,
        genero=persona.genero,
        correo=persona.correo,
        celular=persona.celular,
        nro_documento=persona.nro_documento,
        tipo_documento=persona.tipo_documento
    )
    
    try:
        db.add(db_persona)
        print("Persona added")
        db.commit()
        db.refresh(db_persona)
        return db_persona
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating persona")

@router.put("/personas/{persona_id}", response_model=PersonalDataResponse)
async def update_persona(
    persona_id: int, 
    persona: PersonalData, 
    db: Session = Depends(get_db)
):
    db_persona = db.query(PersonalDataDB).filter(PersonalDataDB.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    for field, value in persona.dict(exclude_unset=True).items():
        setattr(db_persona, field, value)
    
    try:
        db.commit()
        db.refresh(db_persona)
        return db_persona
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating persona")

@router.delete("/personas/{persona_id}")
async def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    db_persona = db.query(PersonalDataDB).filter(PersonalDataDB.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    try:
        db.delete(db_persona)
        db.commit()
        return {"message": "Persona deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting persona")