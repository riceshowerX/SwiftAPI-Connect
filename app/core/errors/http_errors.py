from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from typing import Type

class HTTPError(Exception):
    """自定义 HTTP 异常基类"""
    status_code: int
    detail: str

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class BadRequestError(HTTPError):
    """400 错误请求异常"""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(400, detail)

class UnauthorizedError(HTTPError):
    """401 未授权异常"""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(401, detail)

async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """统一 HTTP 异常处理器"""
    
    # 异常类型映射
    exception_map = {
        HTTPException: (exc.status_code, exc.detail),
        HTTPError: (exc.status_code, exc.detail),
    }
    
    # 获取异常信息
    status_code, detail = exception_map.get(
        type(exc),
        (500, "Internal server error")
    )
    
    # 记录错误日志
    logging.error(
        f"Exception occurred: {request.method} {request.url.path}",
        exc_info=True,
        extra={
            "status_code": status_code,
            "detail": detail,
            "request_headers": dict(request.headers),
        }
    )
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": status_code,
                "message": detail,
                "endpoint": request.url.path,
            }
        }
    )