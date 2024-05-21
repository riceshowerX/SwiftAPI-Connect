# main.py
from fastapi import FastAPI

from app.core.routers import http_mock 
import logging

# 设置日志级别为 DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="app.log"
)

app = FastAPI(
    title="HTTP Mock Server",
    description="A simple HTTP mock server built with FastAPI",
    version="0.1.0"
)

# Include routers
app.include_router(http_mock.router)

logging.info("FastAPI application setup complete.")