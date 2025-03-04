from sqlalchemy import Column, Integer, String, Date, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class GeneroDB(PyEnum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    NO_BINARIO = "No binario"
    PREFIERO_NO_REPORTAR = "Prefiero no reportar"

class TipoDocumentoDB(PyEnum):
    TARJETA_IDENTIDAD = "Tarjeta de identidad"
    CEDULA = "Cédula"

class PersonalDataDB(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    primer_nombre = Column(String(30), nullable=False)
    segundo_nombre = Column(String(30), nullable=True)  # Opcional
    apellidos = Column(String(60), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(Enum(GeneroDB), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)  # Email único
    celular = Column(String(10), nullable=False)
    nro_documento = Column(String(10), unique=True, nullable=False)
    tipo_documento = Column(Enum(TipoDocumentoDB), nullable=False)

    # Índices para búsquedas rápidas
    __table_args__ = (
        Index("idx_correo", "correo"),
        Index("idx_nro_documento", "nro_documento"),
    )