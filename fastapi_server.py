# fastapi_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app
import logging
import uvicorn
import os
from dotenv import load_dotenv

# 加载配置文件
load_dotenv()

# 获取配置文件中的配置信息
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8015))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(',')
API_KEY = os.getenv("API_KEY")

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def run_fastapi():
    try:
        logging.info("Starting FastAPI server...")
        uvicorn.run(
            fastapi_app,
            host=SERVER_HOST,
            port=SERVER_PORT,
            reload=True,  # 开启自动重新加载
            log_config={  # 配置日志记录
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "default",
                        "level": "DEBUG",
                    }
                },
                "loggers": {
                    "uvicorn.access": {
                        "handlers": ["console"],
                        "level": "INFO",
                    },
                    "uvicorn.error": {
                        "handlers": ["console"],
                        "level": "INFO",
                    }
                },
            },
        )
    except Exception as e:
        logging.error(f"An error occurred while running the FastAPI server: {e}")

if __name__ == "__main__":
    # 添加 CORS 中间件 (全局配置)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,  # 允许访问的域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],
    )

    # 添加 API 密钥验证
    @fastapi_app.middleware("http")
    async def api_key_auth(request: Request, call_next):
        api_key = request.headers.get("x-api-key")
        if api_key is None or api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        response = await call_next(request)
        return response

    run_fastapi()