from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings
import logging


# Validate that DATABASE_URL is set
if not settings.database_url:
    logging.warning("DATABASE_URL is not set. Database functionality will not work properly.")

# Create the SQLModel engine with proper configuration for Neon PostgreSQL
if settings.database_url:
    try:
        engine = create_engine(
            settings.database_url,
            echo=False,  # Set to True for SQL query logging during development
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections every 5 minutes
        )
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        raise
else:
    # For testing purposes, we'll create a mock engine
    engine = None


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This function should be called on application startup.
    """
    if engine is None:
        logging.warning("Database engine is not configured. Skipping table creation.")
        return

    from ..models.user import User  # Import here to avoid circular imports
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to provide database sessions.
    This function is used with FastAPI's Depends() for dependency injection.
    """
    if engine is None:
        raise Exception("Database engine is not configured. Cannot create session.")

    with Session(engine) as session:
        yield session


# Additional database-related utilities will be added here
# as the application grows