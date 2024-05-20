# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import http_mock
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="HTTP Mock Server",
    description="A simple HTTP mock server built with FastAPI",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "https://example.com"],  # 根据实际需求设置允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(http_mock.router)

logging.info("FastAPI application setup complete.")
