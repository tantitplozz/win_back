"""
Configuration settings for the Advanced AI Backend.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Union
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    """
    # Base settings
    APP_NAME: str = "Advanced AI Backend"
    DEBUG: bool = Field(default=False, env="DEBUG")
    API_PREFIX: str = "/api/v1"
    
    # API settings
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    
    # Security settings
    SECRET_KEY: str = Field(default="supersecretkey", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # 7 days
    
    # AI Engine settings
    AI_MODEL: str = Field(default="gpt-3.5-turbo", env="AI_MODEL")
    AI_TEMPERATURE: float = Field(default=0.7, env="AI_TEMPERATURE")
    AI_MAX_TOKENS: int = Field(default=2000, env="AI_MAX_TOKENS")
    
    # Telegram Bot settings
    TELEGRAM_BOT_TOKEN: str = Field(default="", env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_IDS: List[int] = Field(default=[], env="TELEGRAM_ADMIN_IDS")
    
    # Database settings
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field(default="advanced_ai", env="MONGODB_DB_NAME")
    
    # Vector DB settings
    VECTOR_DB_URL: str = Field(default="http://localhost:8000", env="VECTOR_DB_URL")
    VECTOR_DB_COLLECTION: str = Field(default="ai_memory", env="VECTOR_DB_COLLECTION")
    
    # File storage
    STORAGE_PATH: Path = Field(default=Path("/app/storage"), env="STORAGE_PATH")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Feature flags
    ENABLE_UNRESTRICTED_MODE: bool = Field(default=True, env="ENABLE_UNRESTRICTED_MODE")
    ENABLE_CODE_EXECUTION: bool = Field(default=True, env="ENABLE_CODE_EXECUTION")
    ENABLE_NSFW_CONTENT: bool = Field(default=True, env="ENABLE_NSFW_CONTENT")
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=60, env="RATE_LIMIT_REQUESTS")  # requests per minute
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Ensure storage directory exists
os.makedirs(settings.STORAGE_PATH, exist_ok=True)
