# fastapi_server.py
import logging
import os
import uvicorn 

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.main import app as fastapi_app
from app.core.errors.http_errors import http_exception_handler
from app.core.config import settings

# 从环境变量中读取日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)

# 添加 API 密钥验证
async def api_key_auth(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key is None or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    response = await call_next(request)
    return response

# 添加 CORS 中间件
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加 API 密钥验证中间件
fastapi_app.middleware("http")(api_key_auth)

# 添加全局异常处理
fastapi_app.add_exception_handler(HTTPException, http_exception_handler)

# 自定义异常处理
@fastapi_app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    """处理所有异常，返回 JSON 格式的错误信息"""
    logging.exception(f"Request: {request.method} {request.url} - Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "internal_server_error",
        },
    )

def run_fastapi():
    try:
        logging.info("Starting FastAPI server...")
        uvicorn.run(
            fastapi_app,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True,
            log_level=LOG_LEVEL.lower(),
        )
    except Exception as e:
        logging.exception(f"An error occurred while running the FastAPI server: {e}") 

if __name__ == "__main__":
    run_fastapi()