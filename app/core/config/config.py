# config.py
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SERVER_HOST: str = os.getenv("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8015))
    CORS_ORIGINS: list =  os.getenv("CORS_ORIGINS", "http://localhost:8501").split(',')
    API_KEY: str = os.getenv("API_KEY")

settings = Settings() 