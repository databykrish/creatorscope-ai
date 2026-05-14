"""Application configuration using Pydantic Settings."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "CreatorScope AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Server
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./creatorscope.db"
    )

    # YouTube API
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    YOUTUBE_MAX_RESULTS: int = 50

    # yt-dlp
    YTDLP_ENABLED: bool = os.getenv("YTDLP_ENABLED", "true").lower() == "true"

    # Rate Limiting
    RATE_LIMIT_DELAY_SECONDS: float = 2.0

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://192.168.56.1:3000",
    ]
    if os.getenv("ALLOWED_ORIGINS"):
        ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

    # Cache
    CACHE_TTL_SECONDS: int = 3600  # 1 hour

    # AI/LLM (optional, for future use)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    AI_MODEL: str = "gpt-3.5-turbo"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
