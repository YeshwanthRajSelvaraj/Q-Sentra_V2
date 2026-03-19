"""
Q-Sentra Configuration Module
Centralizes all application settings via environment variables.
"""
import os
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables."""

    # ── Application ──
    APP_NAME: str = "Q-Sentra"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # ── Database ──
    POSTGRES_URL: str = os.getenv(
        "POSTGRES_URL",
        "postgresql+asyncpg://qsentra:qsentra_pass@localhost:5432/qsentra"
    )
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "qsentra")

    # ── Redis / Celery ──
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER: str = os.getenv("CELERY_BROKER", "redis://localhost:6379/1")
    CELERY_BACKEND: str = os.getenv("CELERY_BACKEND", "redis://localhost:6379/2")

    # ── JWT / Auth ──
    JWT_SECRET: str = os.getenv("JWT_SECRET", "qsentra-super-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", "480"))

    # ── CORS ──
    CORS_ORIGINS: list = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # ── Scanning ──
    SCAN_TIMEOUT: int = int(os.getenv("SCAN_TIMEOUT", "10"))
    MAX_CONCURRENT_SCANS: int = int(os.getenv("MAX_CONCURRENT_SCANS", "20"))

    # ── Mock/Demo Mode ──
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings singleton."""
    return Settings()
