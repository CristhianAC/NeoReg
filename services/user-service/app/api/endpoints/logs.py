from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional
from app.utils.logger import APILogger
from datetime import datetime, timedelta

router = APIRouter(tags=["logs"])

@router.get("/logs", response_model=List[Dict[str, Any]])
async def get_logs(
    limit: int = Query(100, description="Maximum number of logs to return"),
    type_filter: Optional[str] = Query(None, description="Filter logs by type (request, response, error)"),
    path_filter: Optional[str] = Query(None, description="Filter logs by path (partial match)"),
    method_filter: Optional[str] = Query(None, description="Filter logs by HTTP method (GET, POST, etc.)"),
    status_code: Optional[int] = Query(None, description="Filter logs by status code"),
    since: Optional[str] = Query(None, description="Show logs since timestamp (ISO format) or time ago (e.g., '1h', '30m', '1d')")
):
    """
    Retrieve API logs with optional filtering.
    
    - **limit**: Maximum number of logs to return
    - **type_filter**: Filter logs by type (request, response, error)
    - **path_filter**: Filter logs by API path (partial match)
    - **method_filter**: Filter logs by HTTP method (GET, POST, PUT, DELETE)
    - **status_code**: Filter logs by HTTP status code
    - **since**: Show logs since timestamp or time ago (e.g., '1h', '30m', '1d')
    """
    # Get all logs first
    logs = APILogger.get_logs(limit=None)  # No limit initially
    
    # Apply filters
    if type_filter:
        logs = [log for log in logs if log.get("type") == type_filter]
    
    if path_filter:
        logs = [log for log in logs if log.get("path") and path_filter in log.get("path")]
    
    if method_filter:
        logs = [log for log in logs if log.get("method") and log.get("method").upper() == method_filter.upper()]
    
    if status_code:
        logs = [log for log in logs if log.get("status_code") == status_code]
    
    if since:
        try:
            # Try parsing as ISO timestamp
            since_time = None
            try:
                since_time = datetime.fromisoformat(since)
            except ValueError:
                # Try parsing as relative time
                if since.endswith('h'):
                    hours = int(since[:-1])
                    since_time = datetime.now() - timedelta(hours=hours)
                elif since.endswith('m'):
                    minutes = int(since[:-1])
                    since_time = datetime.now() - timedelta(minutes=minutes)
                elif since.endswith('d'):
                    days = int(since[:-1])
                    since_time = datetime.now() - timedelta(days=days)
                else:
                    raise ValueError("Invalid time format")
            
            if since_time:
                logs = [
                    log for log in logs 
                    if "timestamp" in log and datetime.fromisoformat(log["timestamp"]) >= since_time
                ]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid 'since' parameter: {str(e)}")
    
    # Sort logs by timestamp in descending order (most recent first)
    logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Apply limit after all filters and sorting
    return logs[:limit] if limit else logs

@router.get("/logs/test", include_in_schema=True)
@router.get("/logs/test/", include_in_schema=True)
async def test_logs_router():
    return {"status": "logs router is working"}

@router.get("/logs/stats", response_model=Dict[str, Any])
async def get_logs_stats():
    """Get statistics about the logs"""
    all_logs = APILogger.get_logs(limit=None)
    
    # Count types
    requests_count = len([log for log in all_logs if log.get("type") == "request"])
    responses_count = len([log for log in all_logs if log.get("type") == "response"])
    errors_count = len([log for log in all_logs if log.get("type") == "error"])
    
    # Count methods
    methods = {}
    for log in all_logs:
        if log.get("type") == "request" and log.get("method"):
            method = log.get("method")
            methods[method] = methods.get(method, 0) + 1
    
    # Count status codes
    status_codes = {}
    for log in all_logs:
        if log.get("type") == "response" and log.get("status_code"):
            status = log.get("status_code")
            status_codes[status] = status_codes.get(status, 0) + 1
    
    # Get most recent logs timestamps
    last_request = next((log.get("timestamp") for log in reversed(all_logs) if log.get("type") == "request"), None)
    last_error = next((log.get("timestamp") for log in reversed(all_logs) if log.get("type") == "error"), None)
    
    return {
        "total_logs": len(all_logs),
        "requests": requests_count,
        "responses": responses_count,
        "errors": errors_count,
        "methods": methods,
        "status_codes": status_codes,
        "last_request": last_request,
        "last_error": last_error
    }

@router.delete("/logs/clear", response_model=Dict[str, Any])
async def clear_logs():
    """Clear all logs from memory (use with caution)"""
    global api_logs
    count = len(APILogger.get_logs(limit=None))
    # Reset logs
    APILogger.api_logs = []
    return {"message": f"Cleared {count} logs from memory"}