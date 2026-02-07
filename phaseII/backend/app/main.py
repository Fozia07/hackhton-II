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
import time

# Set up logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables
    await create_db_and_tables()
    logger.info("Database tables created successfully")
    yield
    # Shutdown logic here if needed

app = FastAPI(title=settings.app_title, version=settings.app_version, lifespan=lifespan)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    """
    Middleware to log all incoming requests with method, path, status code, and duration.
    """
    start_time = time.time()

    # Log incoming request
    logger.info(f"→ {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Log response
    logger.info(f"← {request.method} {request.url.path} {response.status_code} {duration_ms:.2f}ms")

    return response

# Parse allowed origins
origins = settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"]
logger.info(f"Configured CORS Allowed Origins: {origins}")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    Tests actual database connectivity and measures latency.
    """
    import time
    from datetime import datetime

    try:
        # Test database connectivity with actual query
        start_time = time.time()
        async with AsyncSession(engine) as session:
            from sqlmodel import select
            await session.execute(select(1))
        latency_ms = int((time.time() - start_time) * 1000)

        # Determine status based on latency
        if latency_ms < 100:
            status = "ok"
        elif latency_ms < 500:
            status = "degraded"
        else:
            status = "error"

        response = {
            "status": status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": settings.app_version,
            "database": {
                "status": "connected",
                "latency_ms": latency_ms
            },
            "endpoints": {
                "auth": "available",
                "todos": "available"
            }
        }

        # Return 503 if status is error
        if status == "error":
            from fastapi import Response
            return Response(
                content=str(response),
                status_code=503,
                media_type="application/json"
            )

        return response

    except Exception as e:
        from fastapi import Response
        import json

        error_response = {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": settings.app_version,
            "database": {
                "status": "disconnected",
                "error": str(e)
            },
            "endpoints": {
                "auth": "unavailable",
                "todos": "unavailable"
            }
        }

        return Response(
            content=json.dumps(error_response),
            status_code=503,
            media_type="application/json"
        )


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