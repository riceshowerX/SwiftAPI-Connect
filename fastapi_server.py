# fastapi_server.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app
from app.errors.http_errors import http_exception_handler
import logging
import uvicorn
import os
from dotenv import load_dotenv
from loguru import logger

# 加载配置文件
load_dotenv()

# 获取配置文件中的配置信息
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8015))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(',')
API_KEY = os.getenv("API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "huaizhu").encode()  # 读取加密密钥

# 设置日志
logger.add(
    "app.log",
    format="{time} {level} {message}",
    level="DEBUG",  # 设置日志级别为 DEBUG
    rotation="500 MB",
    compression="zip",
)

# 添加 API 密钥验证
async def api_key_auth(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key is None or api_key != API_KEY:
        logger.warning(f"Invalid API key: {api_key}")  # 记录警告信息
        raise HTTPException(status_code=401, detail="Invalid API key")
    response = await call_next(request)
    return response

def run_fastapi():
    try:
        logger.info("Starting FastAPI server...")
        uvicorn.run(
            fastapi_app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            reload=True,  # 开启自动重新加载
        )
    except Exception as e:
        logger.error(f"An error occurred while running the FastAPI server: {e}")


if __name__ == "__main__":
    # 添加 CORS 中间件 (全局配置)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,  # 允许访问的域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],
    )

    # 添加 API 密钥验证中间件
    fastapi_app.middleware("http")(api_key_auth)

    # 添加全局异常处理
    fastapi_app.add_exception_handler(HTTPException, http_exception_handler)
    
    run_fastapi()