from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from typing import Generator
from .config import settings
import logging


# Validate that DATABASE_URL is set
if not settings.database_url:
    logging.warning("DATABASE_URL is not set. Database functionality will not work properly.")

# Create the async SQLModel engine with proper configuration for Neon PostgreSQL
if settings.database_url:
    try:
        engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=False,  # Set to True for SQL query logging during development
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections every 5 minutes
            connect_args={"ssl": True}
        )
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        raise
else:
    # For testing purposes, we'll create a mock engine
    engine = None


async def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This function should be called on application startup.
    """
    if engine is None:
        logging.warning("Database engine is not configured. Skipping table creation.")
        return

    from ..models.user import User  # Import here to avoid circular imports
    async with engine.begin() as conn:
        # Run the sync operation within the async context
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Dependency to provide database sessions.
    This function is used with FastAPI's Depends() for dependency injection.
    """
    if engine is None:
        raise Exception("Database engine is not configured. Cannot create session.")

    async with AsyncSession(engine) as session:
        yield session


# Additional database-related utilities will be added here
# as the application grows