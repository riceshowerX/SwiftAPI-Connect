from dotenv import load_dotenv
import os
from fastapi import FastAPI
from typing import Optional
import logging

# 环境变量加载优化
def load_environment_variables() -> None:
    """加载环境变量并添加日志记录"""
    try:
        load_dotenv(verbose=True)
        logging.info("成功加载 .env 文件环境变量")
    except Exception as e:
        logging.error(f"环境变量加载失败: {e}")
        raise SystemExit(1)

# 日志配置优化
def configure_logging(log_level: str) -> None:
    """配置双通道日志记录系统（文件+控制台）"""
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 文件日志处理器
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    
    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # 根日志记录器配置
    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=[file_handler, console_handler]
    )

# 应用创建工厂函数
def create_application() -> FastAPI:
    """创建并配置 FastAPI 应用实例"""
    application = FastAPI(
        title="HTTP Mock Server",
        description="基于 FastAPI 的轻量级 HTTP 模拟服务器",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # 路由注册
    from app.core.routers import http_mock
    application.include_router(http_mock.router)
    logging.info("成功注册 HTTP Mock 路由")
    
    return application

# 主执行流程
if __name__ == "__main__":
    # 1. 配置日志级别
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    
    # 2. 加载环境变量
    load_environment_variables()
    
    # 3. 配置日志系统
    configure_logging(LOG_LEVEL)
    
    # 4. 创建应用实例
    app = create_application()
    
    # 5. 启动信息记录
    logging.info("FastAPI 应用初始化完成")
    logging.info(f"当前日志级别: {LOG_LEVEL}")
    logging.info("API 文档地址: http://localhost:8000/docs")