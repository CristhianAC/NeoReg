from sqlalchemy import Column, Integer, String, Date, Enum, Index
from app.core.database import Base
from enum import Enum as PyEnum

class GeneroDB(str, PyEnum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    NO_BINARIO = "NO_BINARIO"
    PREFIERO_NO_REPORTAR = "PREFIERO_NO_REPORTAR"

class TipoDocumentoDB(str, PyEnum):
    TARJETA_IDENTIDAD = "TARJETA_DE_IDENTIDAD"
    CEDULA = "CEDULA"

class PersonalDataDB(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    primer_nombre = Column(String(30), nullable=False)
    segundo_nombre = Column(String(30))
    apellidos = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(Enum(GeneroDB, name='genero_enum'), nullable=False)
    correo = Column(String, unique=True, nullable=False)
    celular = Column(String(10), nullable=False)
    nro_documento = Column(String, unique=True, nullable=False)
    tipo_documento = Column(Enum(TipoDocumentoDB, name='tipo_documento_enum'), nullable=False)

    __table_args__ = (
        Index("idx_correo", "correo"),
        Index("idx_nro_documento", "nro_documento"),
    )