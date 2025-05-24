import os
import shutil
import uuid
from http.client import HTTPException
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from typing import Optional

# Crear directorio para almacenar las fotos si no existe
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

@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    """
    Sube una foto al servidor.
    
    - **file**: Archivo de imagen a subir (máximo 2MB)
    
    Retorna el nombre del archivo generado para poder accederlo posteriormente.
    """
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
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "size": file_size,
            "content_type": file.content_type,
            "url": f"/api/v1/photos/{unique_filename}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    finally:
        await file.close()

@router.get("/{filename}")
async def get_photo(filename: str):
    """
    Obtiene una foto por su nombre de archivo.
    
    - **filename**: Nombre del archivo generado durante la carga
    
    Retorna la imagen para ser mostrada.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
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

@router.delete("/{filename}")
async def delete_photo(filename: str):
    """
    Elimina una foto del servidor.
    
    - **filename**: Nombre del archivo a eliminar
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    try:
        os.remove(file_path)
        return {"message": "Imagen eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")