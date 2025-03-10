from fastapi import APIRouter, HTTPException
from app.services.user_service import get_all_users
from google import genai
from app.core.config import settings
import httpx
import re
from pydantic import BaseModel

router = APIRouter()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)


class SQLQueryRequest(BaseModel):
    question: str


def is_database_related(question: str) -> bool:
 
    
    
    
   
    
    return True

async def process_natural_language_query(query: str, user_data: list) -> str:
    if not is_database_related(query):
        raise HTTPException(
            status_code=400, 
            detail="La pregunta debe estar relacionada con la base de datos de empleados"
        )

    try:
        context = f"""
        Eres un asistente que ayuda a responder preguntas sobre empleados.
        no puedes responder preguntas que no tengan que ver con la base de datos
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


async def generate_sql_query(question: str) -> str:
    if not is_database_related(question):
        raise HTTPException(
            status_code=400, 
            detail="La pregunta debe estar relacionada con la base de datos de empleados"
        )
        
    try:
        context = f"""
        Eres un experto en SQL para PostgreSQL. Necesito que generes una consulta SQL basada en la siguiente pregunta.
        
        La base de datos tiene una tabla 'personas' con los siguientes campos:
        - id (Integer, primary key)
        - primer_nombre (String)
        - segundo_nombre (String, nullable)
        - apellidos (String)
        - fecha_nacimiento (Date)
        - genero (Enum: MASCULINO, FEMENINO, NO_BINARIO, PREFIERO_NO_REPORTAR)
        - correo (String, unique)
        - celular (String)
        - nro_documento (String, unique)
        - tipo_documento (Enum: TARJETA_DE_IDENTIDAD, CEDULA)
        
        Pregunta: {question}
        
        IMPORTANTE: Genera SOLO la consulta SQL sin explicaciones adicionales. La consulta debe ser segura, eficiente y optimizada.
        SOLO usa la palabra clave SELECT al inicio de la consulta. No uses comillas simples para los nombres de columnas.
        No incluyas punto y coma (;) al final de la consulta.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=context,
        )
        
        if response.text:
            sql_query = response.text.strip()
            sql_query = sql_query.replace(';', '')
            if not sql_query.upper().startswith('SELECT'):
                sql_query = f"SELECT {sql_query}"
            
            print(f"Generated SQL query: {sql_query}")
            return sql_query
        else:
            raise HTTPException(status_code=500, detail="No se generó consulta SQL")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating SQL query: {str(e)}")


async def execute_sql_query(sql_query: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.USER_SERVICE_URL}/api/v1/execute-sql",
                json={"query": sql_query}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error executing SQL query: {response.text}"
                )
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {str(e)}")


@router.post("/query")
async def query_employees(query: str):
    try:
        users = await get_all_users()
        response = await process_natural_language_query(query, users)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sql-query")
async def sql_query_endpoint(request: SQLQueryRequest):
    try:
        if not is_database_related(request.question):
            raise HTTPException(
                status_code=400, 
                detail="La pregunta debe estar relacionada con la base de datos de empleados"
            )
            
        sql_query = await generate_sql_query(request.question)
        
        try:
            query_results = await execute_sql_query(sql_query)
        except HTTPException as e:
            print(f"Original query failed: {sql_query}")
            simplified_query = f"SELECT * FROM personas LIMIT 5"
            print(f"Trying simplified query: {simplified_query}")
            query_results = await execute_sql_query(simplified_query)
        
        context = f"""
        Eres un asistente que ayuda a responder preguntas sobre empleados.
        No puedes responder cosas que no tengan que ver con la base de datos.
        por ejemplo, no puedes responder preguntas sobre el clima. o sobre sumas que no tengan que ver con el tema.
        recuerda el contexto y es que solo puedes brindar informacion de los trabajadores.

        IMPORTANTE: NO RESPONDAS LAS PREGUNTAS FUERA DEL ANTERIOR CONTEXTO.
        Pregunta: {request.question}
        
        Resultados de la consulta SQL: {query_results}
        
        Responde a la pregunta en español de forma concisa y natural basándote en los resultados.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=context,
        )
        
        if not response.text:
            raise HTTPException(status_code=500, detail="No se generó respuesta")
            
        return {
            "question": request.question,
            "sql_query": sql_query,
            "results": query_results,
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))