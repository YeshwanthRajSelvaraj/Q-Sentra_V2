"""
Q-Sentra Database Module
Manages PostgreSQL (SQLAlchemy async) and MongoDB (Motor) connections.
"""
import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.config import get_settings

settings = get_settings()


# ── SQLAlchemy Base ──
class Base(DeclarativeBase):
    pass


# ── PostgreSQL ──
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Dependency: yields a PostgreSQL session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_postgres():
    """Create all PostgreSQL tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ── MongoDB ──
_mongo_client: Optional[AsyncIOMotorClient] = None
_mongo_db: Optional[AsyncIOMotorDatabase] = None


async def init_mongo():
    """Initialize MongoDB connection."""
    global _mongo_client, _mongo_db
    _mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
    _mongo_db = _mongo_client[settings.MONGO_DB]
    # Create indexes
    await _mongo_db.cbom.create_index("asset_id", unique=True)
    await _mongo_db.scan_results.create_index("asset_id")
    await _mongo_db.certificates.create_index("certificate_id", unique=True)
    await _mongo_db.blockchain_ledger.create_index("tx_hash", unique=True)


def get_mongo() -> AsyncIOMotorDatabase:
    """Returns the MongoDB database instance."""
    if _mongo_db is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo() first.")
    return _mongo_db


async def close_databases():
    """Gracefully close all database connections."""
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
    await engine.dispose()
