# fastapi_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def run_fastapi():
    import uvicorn
    try:
        logging.info("Starting FastAPI server...")
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8015)  # 允许所有IP访问
    except Exception as e:
        logging.error(f"An error occurred while running the FastAPI server: {e}")


if __name__ == "__main__":
    # 添加 CORS 中间件 (全局配置)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8501"],  # 允许访问的域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],
    )

    run_fastapi()