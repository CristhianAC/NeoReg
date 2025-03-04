from fastapi import APIRouter, HTTPException
from app.services.user_service import get_all_users
from google import genai
from app.core.config import settings

router = APIRouter()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)



async def process_natural_language_query(query: str, user_data: list) -> str:
    try:
        # Create context for the LLM
        context = f"""
        Eres un asistente que ayuda a responder preguntas sobre empleados.
        Aquí están los datos de los empleados: {user_data}
        
        Pregunta: {query}
        
        Responde en español y de forma concisa.
        """

        response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=context,
)
        
        if response.text:
            return response.text
        else:
            raise HTTPException(status_code=500, detail="No se generó respuesta")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/query")
async def query_employees(query: str):
    try:
        users = await get_all_users()
        response = await process_natural_language_query(query, users)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))