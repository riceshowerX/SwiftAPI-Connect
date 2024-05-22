# http_errors.py
from fastapi import HTTPException, JSONResponse 

class HTTPError(HTTPException):
    """自定义 HTTP 异常"""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

def http_error_handler(request, exc: Exception):
    """全局 HTTP 异常处理"""
    return JSONResponse(
        status_code=500 if not isinstance(exc, HTTPException) else exc.status_code,
        content={"detail": exc.detail if isinstance(exc, HTTPException) else "Internal Server Error"},
    )