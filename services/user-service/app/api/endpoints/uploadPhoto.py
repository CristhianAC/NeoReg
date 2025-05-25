import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import PersonalDataDB

# Crear directorio base para almacenar las fotos
UPLOAD_DIRECTORY = "uploads/photos"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Not found"}}
)

# Función auxiliar para obtener la extensión de archivo
def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

# Función para verificar que la persona existe
def verify_person_exists(person_id: int, db: Session):
    person = db.query(PersonalDataDB).filter(PersonalDataDB.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f"Persona con ID {person_id} no encontrada")
    return person

# Función para crear el directorio de la persona si no existe
def get_person_directory(person_id: int) -> str:
    person_dir = os.path.join(UPLOAD_DIRECTORY, str(person_id))
    os.makedirs(person_dir, exist_ok=True)
    return person_dir

@router.post("/upload/{person_id}")
async def upload_photo(person_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Sube una foto al servidor y la asocia con una persona específica.
    
    - **person_id**: ID de la persona a la que pertenece la foto
    - **file**: Archivo de imagen a subir (máximo 2MB)
    
    Retorna el nombre del archivo generado y detalles para accederlo posteriormente.
    """
    # Verificar que la persona existe
    person = verify_person_exists(person_id, db)
    
    try:
        # Verificar tamaño del archivo
        content = await file.read(2 * 1024 * 1024 + 1)  # Lee hasta 2MB + 1 byte
        file_size = len(content)
        
        if file_size > 2 * 1024 * 1024:  # 2 MB
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande (máximo 2MB)")
        
        # Verificar que sea una imagen
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_extension = get_file_extension(file.filename)
        
        if file_extension not in valid_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Formato de archivo no permitido. Use uno de los siguientes: {', '.join(valid_extensions)}"
            )
        
        # Generar nombre único para el archivo
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Obtener/crear directorio para esta persona
        person_dir = get_person_directory(person_id)
        
        # Ruta completa del archivo
        file_path = os.path.join(person_dir, unique_filename)
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        return {
            "person_id": person_id,
            "filename": unique_filename,
            "original_filename": file.filename,
            "size": file_size,
            "content_type": file.content_type,
            "url": f"/api/v1/photos/person/{person_id}/{unique_filename}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    finally:
        await file.close()

@router.get("/person/{person_id}")
async def get_person_photos(person_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las fotos asociadas a una persona específica.
    
    - **person_id**: ID de la persona
    
    Retorna una lista de todas las fotos disponibles para esa persona.
    """
    # Verificar que la persona existe
    verify_person_exists(person_id, db)
    
    person_dir = os.path.join(UPLOAD_DIRECTORY, str(person_id))
    
    # Si el directorio no existe, significa que no hay fotos
    if not os.path.exists(person_dir):
        return []
    
    photos = []
    for filename in os.listdir(person_dir):
        if os.path.isfile(os.path.join(person_dir, filename)):
            photos.append({
                "filename": filename,
                "url": f"/api/v1/photos/person/{person_id}/{filename}"
            })
    
    return photos

@router.get("/person/{person_id}/{filename}")
async def get_person_photo(person_id: int, filename: str, db: Session = Depends(get_db)):
    """
    Obtiene una foto específica de una persona.
    
    - **person_id**: ID de la persona
    - **filename**: Nombre del archivo generado durante la carga
    
    Retorna la imagen para ser mostrada.
    """
    # Verificar que la persona existe
    verify_person_exists(person_id, db)
    
    file_path = os.path.join(UPLOAD_DIRECTORY, str(person_id), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada para esta persona")
    
    # Detectar el tipo de contenido basado en la extensión
    extension = get_file_extension(filename)
    content_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }
    content_type = content_type_map.get(extension, 'application/octet-stream')
    
    return FileResponse(
        file_path, 
        media_type=content_type,
        filename=filename
    )

# Mantener el endpoint original por compatibilidad
@router.get("/{filename}")
async def get_photo(filename: str):
    """
    Obtiene una foto por su nombre de archivo (compatibilidad con versiones anteriores).
    Este endpoint buscará en todos los directorios de personas.
    
    - **filename**: Nombre del archivo generado durante la carga
    
    Retorna la imagen para ser mostrada.
    """
    # Buscar el archivo en todos los directorios de personas
    for root, dirs, files in os.walk(UPLOAD_DIRECTORY):
        if filename in files:
            file_path = os.path.join(root, filename)
            
            # Detectar el tipo de contenido basado en la extensión
            extension = get_file_extension(filename)
            content_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp'
            }
            content_type = content_type_map.get(extension, 'application/octet-stream')
            
            return FileResponse(
                file_path, 
                media_type=content_type,
                filename=filename
            )
    
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

@router.delete("/person/{person_id}/{filename}")
async def delete_person_photo(person_id: int, filename: str, db: Session = Depends(get_db)):
    """
    Elimina una foto específica de una persona.
    
    - **person_id**: ID de la persona
    - **filename**: Nombre del archivo a eliminar
    """
    # Verificar que la persona existe
    verify_person_exists(person_id, db)
    
    file_path = os.path.join(UPLOAD_DIRECTORY, str(person_id), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada para esta persona")
    
    try:
        os.remove(file_path)
        return {"message": f"Imagen {filename} eliminada correctamente de la persona con ID {person_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")

# Mantener el endpoint original por compatibilidad
@router.delete("/{filename}")
async def delete_photo(filename: str):
    """
    Elimina una foto del servidor (compatibilidad con versiones anteriores).
    Este endpoint buscará en todos los directorios de personas.
    
    - **filename**: Nombre del archivo a eliminar
    """
    # Buscar el archivo en todos los directorios de personas
    for root, dirs, files in os.walk(UPLOAD_DIRECTORY):
        if filename in files:
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                return {"message": f"Imagen {filename} eliminada correctamente"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Imagen no encontrada")