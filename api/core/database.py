"""Database connection management for PostgreSQL and MongoDB."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# MongoDB
mongo_client: AsyncIOMotorClient = None
mongo_db = None


async def get_db() -> AsyncSession:
    """Get PostgreSQL session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_mongo():
    """Get MongoDB database instance."""
    return mongo_db


async def init_db():
    """Initialize database connections."""
    global mongo_client, mongo_db
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongo_db = mongo_client.qsentra


async def close_db():
    """Close database connections."""
    global mongo_client
    if mongo_client:
        mongo_client.close()
    await engine.dispose()
