from sqlalchemy import Column, Integer, String, Date, Enum as SQLAlchemyEnum
from app.core.database import Base
import enum

class Gender(str, enum.Enum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    NO_BINARIO = "NO_BINARIO"
    PREFIERO_NO_REPORTAR = "PREFIERO_NO_REPORTAR"

class DocumentType(str, enum.Enum):
    TARJETA_IDENTIDAD = "TARJETA_DE_IDENTIDAD"  
    CEDULA = "CEDULA"

class PersonalDataDB(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    primer_nombre = Column(String)
    segundo_nombre = Column(String, nullable=True)
    apellidos = Column(String)
    fecha_nacimiento = Column(Date)
    genero = Column(SQLAlchemyEnum(Gender))
    correo = Column(String, unique=True)
    celular = Column(String)
    nro_documento = Column(String, unique=True)
    tipo_documento = Column(SQLAlchemyEnum(DocumentType))