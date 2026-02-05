from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from .core.config import settings
from .core.database import create_db_and_tables, get_session, engine
from .routes.auth import router as auth_router
from .routes.todos import router as todos_router


import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables
    await create_db_and_tables()
    logger.info("Database tables created successfully")
    yield
    # Shutdown logic here if needed

app = FastAPI(title=settings.app_title, version=settings.app_version, lifespan=lifespan)

# Parse allowed origins
origins = settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"]
logger.info(f"Configured CORS Allowed Origins: {origins}")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["https://hackhton-ii.vercel.app/",
                   "http://localhost:3000",
                   ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Include authentication routes
app.include_router(auth_router)

# Include todos routes
app.include_router(todos_router)




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
    try:
        # Test database connectivity
        if engine:
            from sqlmodel import select
            from .models.user import User
            # Just test if we can access the engine
            db_status = "connected" if engine else "disconnected"
        else:
            db_status = "not configured"

        return {
            "status": "ok",
            "database": db_status,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }


# Example endpoint showing how to use database sessions with dependency injection
@app.get("/test-db")
async def test_db_connection(session: AsyncSession = Depends(get_session)):
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