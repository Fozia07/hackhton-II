from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from .engine import engine

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session():
    """
    Dependency function that provides a database session for FastAPI endpoints.
    Ensures the session is properly closed after use.
    """
    async with AsyncSessionLocal() as session:
        yield session