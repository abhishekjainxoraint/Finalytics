from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "FP&A Intelligence API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 5000
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Database - Optional for development
    MONGODB_URI: str = "mongodb://localhost:27017/fpa-analysis"
    DATABASE_NAME: str = "fpa-analysis"
    DISABLE_DATABASE: bool = True  # Set to True to run without MongoDB
    
    # Redis - Optional for development  
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    DISABLE_REDIS: bool = True  # Set to True to run without Redis
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_FILE_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "text/csv"
    ]
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hour
    
    # Background Jobs
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Auto-detect if we should disable external dependencies
if settings.ENVIRONMENT == "development":
    # Try to detect if MongoDB/Redis are available
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 27017))
        sock.close()
        if result != 0:
            settings.DISABLE_DATABASE = True
    except:
        settings.DISABLE_DATABASE = True
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 6379))
        sock.close()
        if result != 0:
            settings.DISABLE_REDIS = True
    except:
        settings.DISABLE_REDIS = True

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 