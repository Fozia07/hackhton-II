"""
Standalone entry point for the Todo AI Chatbot MCP Server.
This module provides a standalone entry point for the MCP server that can be run independently.
"""
from app.mcp_server.server import server
from app.mcp_server.config import TRANSPORT_TYPE, DEFAULT_HOST, DEFAULT_PORT, DEBUG_MODE


def run_standalone_server():
    """
    Run the MCP server as a standalone application.
    """
    print(f"Starting MCP Server: {server.name}")
    print(f"Transport: {TRANSPORT_TYPE}")
    print(f"Host: {DEFAULT_HOST}")
    print(f"Port: {DEFAULT_PORT}")
    print("Press Ctrl+C to stop the server")

    server.run(
        transport=TRANSPORT_TYPE,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        debug=DEBUG_MODE,
        reload=DEBUG_MODE  # Enable auto-reload in debug mode
    )


if __name__ == "__main__":
    run_standalone_server()