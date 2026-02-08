"""
Configuration settings for the Todo AI Chatbot MCP Server.
This module contains all configuration parameters for the MCP server.
"""

# Server Configuration
SERVER_NAME = "todo-ai-chatbot-mcp-server"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "MCP server for Todo AI Chatbot that provides tools for managing tasks"

# Transport Configuration
TRANSPORT_TYPE = "streamable-http"  # Compatible with OpenAI Agents SDK
DEFAULT_HOST = "0.0.0.0"  # Allow external connections
DEFAULT_PORT = 8002  # Use different port to avoid conflicts with main app

# Debug Configuration
DEBUG_MODE = True  # Set to False in production

# Server Instructions
SERVER_INSTRUCTIONS = "MCP server for Todo AI Chatbot that provides tools for managing tasks. This server provides 5 tools: add_task, list_tasks, complete_task, delete_task, and update_task. Each tool requires a valid user_id for authentication and authorization."

# Tool Configuration
REGISTERED_TOOLS = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task"
]

# Error Configuration
ERROR_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Authentication Configuration
TOKEN_EXPIRATION_MINUTES = 30