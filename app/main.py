# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import http_mock

app = FastAPI(title="HTTP Mock Server", description="A simple HTTP mock server built with FastAPI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(http_mock.router)