from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from app.core.database import get_db
import re

router = APIRouter()

class SQLQuery(BaseModel):
    query: str

def is_safe_query(query: str) -> bool:
    query_lower = query.lower().strip()
    
    if not query_lower.startswith('select'):
        return False
    
    if ';' in query_lower:
        return False
    
    dangerous_keywords = [
        'insert', 'update', 'delete', 'drop', 'alter', 'truncate', 
        'create', 'grant', 'revoke', 'commit', 'rollback', 'exec', 
        'execute'
    ]
    
    for keyword in dangerous_keywords:
        pattern = r'\b' + keyword + r'\b'
        if re.search(pattern, query_lower):
            return False
    
    if 'union' in query_lower and not re.search(r'union\s+select', query_lower):
        return False
    
    return True

@router.post("/execute-sql")
async def execute_sql(query_data: SQLQuery, db: Session = Depends(get_db)):
    if not is_safe_query(query_data.query):
        raise HTTPException(
            status_code=400, 
            detail="Invalid query. Only SELECT statements are allowed and certain operations are restricted."
        )
    
    try:
        result = db.execute(text(query_data.query))
        columns = result.keys()
        rows = []
        for row in result:
            rows.append({column: value for column, value in zip(columns, row)})
        return rows
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error executing query: {str(e)}")