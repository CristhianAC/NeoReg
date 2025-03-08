from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.models import Gender, DocumentType

class PersonalData(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellidos: str
    fecha_nacimiento: date
    genero: Gender
    correo: str
    celular: str
    nro_documento: str
    tipo_documento: DocumentType

class PersonalDataResponse(PersonalData):
    id: int

    class Config:
        from_attributes = True