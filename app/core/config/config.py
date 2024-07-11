# config.py
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SERVER_HOST: str = os.getenv("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8015))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:8501").split(",")
    API_KEY: str = os.getenv("API_KEY")

    MONITORING_INTERVAL: int = int(os.getenv("MONITORING_INTERVAL", 5))  
    CPU_THRESHOLD: int = int(os.getenv("CPU_THRESHOLD", 80)) 
    MEMORY_THRESHOLD: int = int(os.getenv("MEMORY_THRESHOLD", 80)) 

    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD")

    # ... 其他配置

settings = Settings()