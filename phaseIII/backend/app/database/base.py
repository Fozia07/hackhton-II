from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from .engine import engine

# Base class for all models
SQLModel.metadata.bind = engine

async def create_tables():
    """
    Create all tables in the database.
    This function should be called on application startup.
    """
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def drop_tables():
    """
    Drop all tables in the database.
    Use with caution - this will delete all data!
    """
    async with engine.begin() as conn:
        # Drop tables
        await conn.run_sync(SQLModel.metadata.drop_all)