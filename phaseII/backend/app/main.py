from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import os
from .core.config import settings
from .core.database import create_db_and_tables, get_session, engine
from .routes.auth import router as auth_router
from .routes.todos import router as todos_router


import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_title, version=settings.app_version)

# Parse allowed origins
origins = settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"]
logger.info(f"Configured CORS Allowed Origins: {origins}")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include authentication routes
app.include_router(auth_router)

# Include todos routes
app.include_router(todos_router)


@app.on_event("startup")
def on_startup():
    """
    Initialize database tables when the application starts.
    This ensures that all required tables are created before the application begins serving requests.
    """
    create_db_and_tables()


@app.get("/")
async def root():
    """
    Root endpoint that provides basic information about the API.
    """
    return {"message": "Phase 2 Backend API", "status": "running"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint that returns the status of the application.
    """
    return {"status": "ok"}


# Example endpoint showing how to use database sessions with dependency injection
@app.get("/test-db")
async def test_db_connection(session: Session = Depends(get_session)):
    """
    Test endpoint to verify database session management is working correctly.
    This endpoint demonstrates how to use the database session dependency.
    """
    # This endpoint can be used to test database connectivity
    # In a real application, this would perform actual database operations
    if engine:
        return {"status": "Database connection working", "db_url": str(engine.url)}
    else:
        return {"status": "Database not configured", "db_url": "None"}


# Additional endpoints will be added here as the application grows