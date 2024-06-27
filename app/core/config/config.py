# config.py
from pydantic import BaseSettings, Field
from typing import List
import os

class Settings(BaseSettings):
    """应用程序配置"""
    
    SERVER_HOST: str = Field(default="127.0.0.1", env="SERVER_HOST")
    SERVER_PORT: int = Field(default=8015, env="SERVER_PORT")
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:8501"], env="CORS_ORIGINS")
    API_KEY: str = Field(default=None, env="API_KEY")

    MONITORING_INTERVAL: int = Field(default=5, env="MONITORING_INTERVAL")
    CPU_THRESHOLD: int = Field(default=80, env="CPU_THRESHOLD")
    MEMORY_THRESHOLD: int = Field(default=80, env="MEMORY_THRESHOLD")

    SMTP_SERVER: str = Field(default=None, env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SENDER_EMAIL: str = Field(default=None, env="SENDER_EMAIL")
    SENDER_PASSWORD: str = Field(default=None, env="SENDER_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# 加载配置
settings = Settings()

# 如果需要，你可以打印配置项来验证是否正确加载
print(settings.dict())