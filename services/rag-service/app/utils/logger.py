import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from fastapi import Request, Response
import uuid

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# In-memory log storage
api_logs: List[Dict[str, Any]] = []

# Maximum logs to keep in memory
MAX_LOGS = 1000

class APILogger:
    @staticmethod
    def log_request(request_id: str, method: str, path: str, headers: Dict = None, request_body: Any = None, query_params: Dict = None, client_ip: str = None):
        log_entry = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "request",
            "method": method,
            "path": path,
            "headers": headers,
            "body": request_body,
            "query_params": query_params,
            "client_ip": client_ip
        }
        logging.info(f"API Request: {json.dumps(log_entry, default=str)}")
        api_logs.append(log_entry)
        
        # Keep logs within limit
        if len(api_logs) > MAX_LOGS:
            api_logs.pop(0)
        
        return log_entry
    
    @staticmethod
    def log_response(request_id: str, status_code: int, headers: Dict = None, response_body: Any = None, processing_time: float = None):
        log_entry = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "status_code": status_code,
            "headers": headers,
            "body": response_body,
            "processing_time_ms": processing_time * 1000 if processing_time is not None else None
        }
        logging.info(f"API Response: {json.dumps(log_entry, default=str)}")
        api_logs.append(log_entry)
        
        # Keep logs within limit
        if len(api_logs) > MAX_LOGS:
            api_logs.pop(0)
        
        return log_entry
    
    @staticmethod
    def log_error(request_id: str, error_message: str, status_code: int = 500, stack_trace: str = None):
        log_entry = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "status_code": status_code,
            "message": error_message,
            "stack_trace": stack_trace
        }
        logging.error(f"API Error: {json.dumps(log_entry, default=str)}")
        api_logs.append(log_entry)
        
        # Keep logs within limit
        if len(api_logs) > MAX_LOGS:
            api_logs.pop(0)
        
        return log_entry
    
    @staticmethod
    def log_ai_request(request_id: str, prompt: str, model: str = None, parameters: Dict = None):
        """Log AI model requests specifically"""
        log_entry = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "ai_request",
            "model": model,
            "prompt": prompt,
            "parameters": parameters
        }
        logging.info(f"AI Request: {json.dumps(log_entry, default=str)}")
        api_logs.append(log_entry)
        
        # Keep logs within limit
        if len(api_logs) > MAX_LOGS:
            api_logs.pop(0)
        
        return log_entry
    
    @staticmethod
    def log_ai_response(request_id: str, response: str, processing_time: float = None):
        """Log AI model responses specifically"""
        log_entry = {
            "id": request_id,
            "timestamp": datetime.now().isoformat(),
            "type": "ai_response",
            "response": response,
            "processing_time_ms": processing_time * 1000 if processing_time is not None else None
        }
        logging.info(f"AI Response: {json.dumps(log_entry, default=str)}")
        api_logs.append(log_entry)
        
        # Keep logs within limit
        if len(api_logs) > MAX_LOGS:
            api_logs.pop(0)
        
        return log_entry
    
    @staticmethod
    def get_logs(limit: int = 100, type_filter: str = None):
        """Retrieve logs with optional filtering"""
        if type_filter:
            filtered_logs = [log for log in api_logs if log.get("type") == type_filter]
            return filtered_logs[-limit:] if limit else filtered_logs
        return api_logs[-limit:] if limit else api_logs


# Middleware to log requests and responses
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Get client IP
    client_ip = request.client.host if request.client else None
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    # Get request headers (excluding sensitive ones)
    headers = dict(request.headers)
    if "authorization" in headers:
        headers["authorization"] = "[REDACTED]"
    if "cookie" in headers:
        headers["cookie"] = "[REDACTED]"
    
    # Try to get request body
    request_body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body_bytes = await request.body()
            # Create a new request with the same body for downstream handlers
            request._body = body_bytes
            
            if body_bytes:
                try:
                    request_body = json.loads(body_bytes)
                    # Optionally redact sensitive fields
                    if isinstance(request_body, dict) and "password" in request_body:
                        request_body["password"] = "[REDACTED]"
                except json.JSONDecodeError:
                    # If not JSON, store as string with limited length
                    request_body = body_bytes.decode('utf-8', errors='replace')[:1000]
                    if len(body_bytes) > 1000:
                        request_body += "...[truncated]"
        except Exception as e:
            logging.warning(f"Error parsing request body: {str(e)}")
    
    # Log the request
    APILogger.log_request(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        headers=headers,
        request_body=request_body,
        query_params=query_params,
        client_ip=client_ip
    )
    
    try:
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Get response headers (excluding sensitive ones)
        response_headers = dict(response.headers)
        if "set-cookie" in response_headers:
            response_headers["set-cookie"] = "[REDACTED]"
        
        # Get response body
        response_body = None
        response_body_bytes = b""
        
        # Create a new stream for the response body
        async for chunk in response.body_iterator:
            response_body_bytes += chunk
        
        # Try to parse the response body
        if response_body_bytes:
            try:
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    response_body = json.loads(response_body_bytes)
                else:
                    # For non-JSON responses, limit the size
                    response_body = response_body_bytes.decode('utf-8', errors='replace')[:1000]
                    if len(response_body_bytes) > 1000:
                        response_body += "...[truncated]"
            except Exception as e:
                logging.warning(f"Error parsing response body: {str(e)}")
                response_body = str(response_body_bytes)[:1000]
                if len(response_body_bytes) > 1000:
                    response_body += "...[truncated]"
        
        # Create a new response with the original body
        new_response = Response(
            content=response_body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
        
        # Log the response
        APILogger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            headers=response_headers,
            response_body=response_body,
            processing_time=process_time
        )
        
        return new_response
    except Exception as e:
        # Log any errors with stack trace
        import traceback
        stack_trace = traceback.format_exc()
        process_time = time.time() - start_time
        APILogger.log_error(
            request_id=request_id,
            error_message=str(e),
            stack_trace=stack_trace
        )
        raise e