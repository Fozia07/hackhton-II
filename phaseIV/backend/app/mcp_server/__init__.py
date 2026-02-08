"""
Initialization module for the Todo AI Chatbot MCP Server.
Exports key classes and functions for easy access.
"""

from .config import (
    SERVER_NAME,
    SERVER_VERSION,
    SERVER_DESCRIPTION,
    TRANSPORT_TYPE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEBUG_MODE,
    SERVER_INSTRUCTIONS,
    REGISTERED_TOOLS
)

__all__ = [
    # Server configuration
    "SERVER_NAME",
    "SERVER_VERSION",
    "SERVER_DESCRIPTION",
    "TRANSPORT_TYPE",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "DEBUG_MODE",
    "SERVER_INSTRUCTIONS",
    "REGISTERED_TOOLS",
]