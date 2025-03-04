from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import settings

class VectorService:
    def __init__(self):
        self.client = QdrantClient(settings.VECTOR_DB_HOST, port=settings.VECTOR_DB_PORT)
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.collection_name = "employees"

    async def ensure_collection_exists(self):
        """Ensure collection exists before operations"""
        collections = self.client.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # dimensión del modelo sentence-transformer
                    distance=models.Distance.COSINE
                )
            )

    async def upsert_employees(self, employees: List[dict]):
        await self.ensure_collection_exists()
        
        texts = [
            f"{emp['primer_nombre']} {emp['apellidos']} - {emp['correo']}"
            for emp in employees
        ]
        vectors = self.encoder.encode(texts).tolist()
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=i,
                    vector=vector,
                    payload=employee
                )
                for i, (vector, employee) in enumerate(zip(vectors, employees))
            ]
        )

    async def search_similar(self, query: str, limit: int = 5):
        await self.ensure_collection_exists()
        
        query_vector = self.encoder.encode(query).tolist()
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return [hit.payload for hit in results]