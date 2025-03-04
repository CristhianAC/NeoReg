from contextlib import asynccontextmanager
from fastapi import APIRouter, HTTPException, FastAPI
from app.services.user_service import get_all_users
from app.services.vector_service import VectorService
from google import genai
from app.core.config import settings

router = APIRouter()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)
vector_service = VectorService()
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando la aplicación...")
    try:
        # Inicia la colección en vector_service
        await vector_service.ensure_collection_exists()
        
        # Obtiene todos los usuarios y actualiza los empleados en vector_service
        users = await get_all_users()
        if users:
            await vector_service.upsert_employees(users)
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")
        raise

    yield

    print("Cerrando la aplicación...")

async def process_natural_language_query(query: str) -> str:
    try:
        # Get relevant employees using vector search
        relevant_employees = await vector_service.search_similar(query)
        
        context = f"""
        Eres un asistente que ayuda a responder preguntas sobre empleados.
        Aquí están los datos más relevantes de los empleados: {relevant_employees}
        
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
        response = await process_natural_language_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))