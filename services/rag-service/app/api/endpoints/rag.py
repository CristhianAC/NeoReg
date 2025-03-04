from fastapi import APIRouter, HTTPException
from app.services.user_service import get_all_users
from openai import OpenAI
from app.core.config import settings

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def process_natural_language_query(query: str, user_data: list) -> str:
    try:
        # Create context for the LLM
        context = f"""
        Eres un asistente que ayuda a responder preguntas sobre empleados.
        Aquí están los datos de los empleados: {user_data}
        
        Pregunta: {query}
        """

        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en analizar datos de empleados."},
                {"role": "user", "content": context}
            ]
        )
        
        return response.choices[0].message.content
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