# http_errors.py
from fastapi import HTTPException, JSONResponse 
class HTTPError(Exception):
    """自定义 HTTP 异常"""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def http_exception_handler(request, exc: HTTPException):
    """全局 HTTP 异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )