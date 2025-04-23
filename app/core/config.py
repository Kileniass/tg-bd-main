from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Car Dating App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./car_dating.db"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 