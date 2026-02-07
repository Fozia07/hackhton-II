"""
Main application file for the Todo AI Chatbot Phase III.
Sets up the FastAPI application and includes the AI chat routes.
"""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager

from app.database.base import create_tables

# Import only the existing chat router from your Phase III structure
from app.api.v1.endpoints.chat import router as chat_router

# Load .env as early as possible
load_dotenv()  

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler: create tables on startup.
    """
    # Startup: Create database tables if they don't exist
    await create_tables()
    yield
    # Shutdown: optional cleanup (add if needed later)

# Initialize FastAPI app
app = FastAPI(
    title="Todo AI Chatbot - Phase III",
    description="AI-powered natural language todo manager with Gemini via OpenAI-compatible layer",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware (allow from .env or wildcard for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the Phase III chat router
app.include_router(chat_router, prefix="/api", tags=["AI Chatbot"])

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the application is running.
    """
    return {"status": "healthy", "service": "Todo AI Chatbot - Phase III"}

# Root endpoint
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for the application.
    """
    return {"message": "Welcome to Todo AI Chatbot - Phase III API", "docs": "/docs"}