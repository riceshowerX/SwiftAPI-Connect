import logging
import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.main import app as fastapi_app
from app.core.errors.http_errors import http_exception_handler
from app.core.config import settings

# 配置日志
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)

def configure_middleware(app: FastAPI) -> None:
    """配置中间件"""
    
    # CORS中间件（优先处理跨域请求）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API密钥验证中间件
    @app.middleware("http")
    async def api_key_auth(request: Request, call_next):
        api_key = request.headers.get("x-api-key")
        if api_key != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return await call_next(request)

def configure_exception_handlers(app: FastAPI) -> None:
    """配置异常处理器"""

    # 注册HTTP异常处理器
    app.add_exception_handler(HTTPException, http_exception_handler)

    # 全局异常处理器
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logging.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error_code": "internal_server_error",
            },
        )

# 应用配置
configure_middleware(fastapi_app)
configure_exception_handlers(fastapi_app)

def run_fastapi() -> None:
    """启动FastAPI服务器"""
    try:
        logging.info("Initializing server with:"
                     f"\n- Host: {settings.SERVER_HOST}"
                     f"\n- Port: {settings.SERVER_PORT}"
                     f"\n- Log level: {LOG_LEVEL}")
        uvicorn.run(
            fastapi_app,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True,
            log_level=LOG_LEVEL.lower(),
        )
    except Exception as e:
        logging.exception(f"Server startup failed: {e}")
        raise

if __name__ == "__main__":
    run_fastapi()