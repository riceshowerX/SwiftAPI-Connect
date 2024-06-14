# main.py
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import logging

# 加载环境变量
load_dotenv()

# 从环境变量获取日志级别，默认为 INFO
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

# 设置日志级别和格式
log_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format=log_format,
    datefmt=date_format,
    filename="app.log"
)

# 添加控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, log_level, logging.INFO))
console_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
logging.getLogger().addHandler(console_handler)

# 创建 FastAPI 应用程序实例
app = FastAPI(
    title="HTTP Mock Server",
    description="A simple HTTP mock server built with FastAPI",
    version="0.1.0"
)

# 注册路由
from app.core.routers import http_mock
app.include_router(http_mock.router)

logging.info("FastAPI application setup complete.")
