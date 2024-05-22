# config.py
from pydantic import BaseSettings, AnyHttpUrl
from typing import List
import os

class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8015
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8501"]
    API_KEY: str = os.getenv("API_KEY")

    class Config:
        env_file = '.env'

settings = Settings() 