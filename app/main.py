# main.py
from dotenv import load_dotenv
import os
from fastapi import FastAPI

from app.core.routers import http_mock
import logging

# 从环境变量中读取日志级别，默认为 INFO
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

# 设置日志级别
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="app.log"
)

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="HTTP Mock Server",
    description="A simple HTTP mock server built with FastAPI",
    version="0.1.0"
)

# Include routers
app.include_router(http_mock.router)

logging.info("FastAPI application setup complete.")