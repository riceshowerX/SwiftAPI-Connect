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
    elif isinstance(exc, HTTPError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error."},
        )

# 在 FastAPI 应用中注册异常处理器
from fastapi import FastAPI

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)

@app.exception_handler(HTTPError)
async def custom_http_error_handler(request: Request, exc: HTTPError):
    return await http_exception_handler(request, exc)

# 示例路由
@app.get("/example")
async def example_route():
    raise HTTPError(status_code=400, detail="This is a custom HTTP error")

# 启动应用（在实际使用中，使用命令 uvicorn main:app --reload 启动）
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)