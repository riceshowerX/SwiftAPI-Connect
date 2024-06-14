# http_errors.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
import logging

class HTTPError(Exception):
    """自定义 HTTP 异常"""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def http_exception_handler(request: Request, exc: Union[HTTPException, HTTPError]):
    """全局 HTTP 异常处理"""
    logging.error(f"Request: {request.method} {request.url} - Error: {exc}")

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error."},
        )