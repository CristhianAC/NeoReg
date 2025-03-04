from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
from .models import GeneroDB, TipoDocumentoDB, PersonalDataDB  # Ajusta importaciones
from generoEnum import Genero

class PersonalData(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str]
    apellidos: str
    fecha_nacimiento: date  
    genero: Genero  
    correo: EmailStr
    celular: str
    nro_documento: str
    tipo_documento: str  
    def to_db_model(self):
        return PersonalDataDB(
            primer_nombre=self.primer_nombre,
            segundo_nombre=self.segundo_nombre,
            apellidos=self.apellidos,
            fecha_nacimiento=self.fecha_nacimiento,
            genero=GeneroDB[self.genero.name],  # Si usas Enum de Pydantic
            correo=self.correo,
            celular=self.celular,
            nro_documento=self.nro_documento,
            tipo_documento=TipoDocumentoDB[self.tipo_documento]
        )

    # Método para crear desde modelo de SQLAlchemy
    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            primer_nombre=db_model.primer_nombre,
            segundo_nombre=db_model.segundo_nombre,
            apellidos=db_model.apellidos,
            fecha_nacimiento=db_model.fecha_nacimiento,
            genero=db_model.genero,
            correo=db_model.correo,
            celular=db_model.celular,
            nro_documento=db_model.nro_documento,
            tipo_documento=db_model.tipo_documento
        )
    
    @field_validator("primer_nombre", "segundo_nombre")
    def validate_name(cls, v):
        if v and (not v.isalpha() or len(v) > 30):
            raise ValueError("Nombre inválido")
        return v
    
    @field_validator("celular")
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Celular debe tener 10 dígitos")
        return v