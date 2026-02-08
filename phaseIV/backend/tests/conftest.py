import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.base import SQLModel
from app.database.engine import engine
from app.database.session import AsyncSessionLocal


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Clean up after tests
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()