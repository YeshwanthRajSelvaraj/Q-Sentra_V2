"""Q-Sentra Core Configuration."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Q-Sentra"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://qsentra_admin:QS3ntr@PNB2026!@localhost:5432/qsentra"
    MONGODB_URL: str = "mongodb://qsentra_admin:QS3ntr@M0ng0!@localhost:27017/qsentra?authSource=admin"

    # Redis
    REDIS_URL: str = "redis://:QS3ntr@R3d1s!@localhost:6379/0"

    # JWT
    JWT_SECRET: str = "QS3ntr@JWT2026SecretKey!"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 480  # 8 hours

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://qsentra.pnb.co.in",
    ]

    # Security
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_PER_SECOND: int = 10
    PASSWORD_MIN_LENGTH: int = 12
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_MINUTES: int = 30

    # Scanning
    SCAN_TIMEOUT_SECONDS: int = 5
    MAX_CONCURRENT_SCANS: int = 10
    CT_LOG_INTERVAL_HOURS: int = 6

    # Blockchain
    BLOCKCHAIN_NETWORK: str = "hyperledger"

    # HNDL Parameters
    YEARS_TO_CRQC: float = 7.0

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
