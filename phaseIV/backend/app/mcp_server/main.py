"""
Entry point for the Todo AI Chatbot MCP Server.
This module provides the main application entry point for the MCP server.
"""
import asyncio
from .server import server
from .config import TRANSPORT_TYPE, DEFAULT_HOST, DEFAULT_PORT, DEBUG_MODE


def run_server():
    """
    Run the MCP server with configured settings.
    """
    server.run(
        transport=TRANSPORT_TYPE,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        debug=DEBUG_MODE,
        reload=DEBUG_MODE  # Enable auto-reload in debug mode
    )


if __name__ == "__main__":
    run_server()