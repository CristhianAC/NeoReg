import httpx
from app.core.config import settings

async def get_all_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USER_SERVICE_URL}/api/v1/personas/")
        return response.json()