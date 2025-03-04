from fastapi import APIRouter, HTTPException
from app.services.user_service import get_all_users
from datetime import datetime
import openai
from app.core.config import settings

router = APIRouter()

def process_natural_language_query(query: str, user_data: list):
    # Crear el contexto para el LLM
    context = f"""
    Eres un asistente que ayuda a responder preguntas sobre empleados.
    Aquí están los datos de los empleados: {user_data}
    
    Pregunta: {query}
    """

    response = openai.ChatCompletion.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "Eres un asistente experto en analizar datos de empleados."},
            {"role": "user", "content": context}
        ]
    )
    
    return response.choices[0].message.content

@router.post("/query")
async def query_employees(query: str):
    try:
        # Obtener datos de usuarios
        users = await get_all_users()
        
        # Procesar la consulta
        response = process_natural_language_query(query, users)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))