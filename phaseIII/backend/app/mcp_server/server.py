"""
Core MCP Server implementation for the Todo AI Chatbot.
This module contains the main server instance with all 5 tools registered.
"""
from mcp_use.server import MCPServer
from typing import Optional
from typing_extensions import Annotated

# Import the MCP tools from the tools module
from app.mcp_tools.add_task import add_task as tool_add_task
from app.mcp_tools.list_tasks import list_tasks as tool_list_tasks
from app.mcp_tools.complete_task import complete_task as tool_complete_task
from app.mcp_tools.delete_task import delete_task as tool_delete_task
from app.mcp_tools.update_task import update_task as tool_update_task

# Import configuration
from .config import SERVER_NAME, SERVER_VERSION, SERVER_INSTRUCTIONS, DEBUG_MODE


# Initialize the MCP Server
server = MCPServer(
    name=SERVER_NAME,
    version=SERVER_VERSION,
    instructions=SERVER_INSTRUCTIONS,
    debug=DEBUG_MODE,
    pretty_print_jsonrpc=True,  # Beautiful JSON-RPC logs
)


@server.tool()
async def add_task(
    user_id: Annotated[str, "The ID of the user creating the task"],
    title: Annotated[str, "The title/description of the task to be created"],
    description: Annotated[Optional[str], "Additional details about the task"] = None
) -> dict:
    """
    Create a new task for the authenticated user in the database.

    Returns:
    {
      "task_id": "string",
      "status": "created",
      "title": "string"
    }
    """
    return await tool_add_task(user_id, title, description)


@server.tool()
async def list_tasks(
    user_id: Annotated[str, "The ID of the user whose tasks to retrieve"],
    status: Annotated[Optional[str], "Filter tasks by completion status ('all', 'pending', 'completed')"] = None
) -> list:
    """
    Retrieve all tasks for the authenticated user with optional filtering by status.

    Returns:
    [
      {
        "id": "string",
        "title": "string",
        "completed": false,
        "priority": "string",
        "due_date": "string",
        "category": "string",
        "created_at": "string",
        "updated_at": "string",
        "completed_at": "string"
      }
    ]
    """
    return await tool_list_tasks(user_id, status)


@server.tool()
async def complete_task(
    user_id: Annotated[str, "The ID of the user attempting to complete the task"],
    task_id: Annotated[str, "The ID of the task to mark as completed"]
) -> dict:
    """
    Mark a specific task as completed for the authenticated user.

    Returns:
    {
      "task_id": "string",
      "status": "completed",
      "title": "string"
    }
    """
    return await tool_complete_task(user_id, task_id)


@server.tool()
async def delete_task(
    user_id: Annotated[str, "The ID of the user attempting to delete the task"],
    task_id: Annotated[str, "The ID of the task to delete"]
) -> dict:
    """
    Remove a specific task from the user's task list.

    Returns:
    {
      "task_id": "string",
      "status": "deleted",
      "title": "string"
    }
    """
    return await tool_delete_task(user_id, task_id)


@server.tool()
async def update_task(
    user_id: Annotated[str, "The ID of the user attempting to update the task"],
    task_id: Annotated[str, "The ID of the task to update"],
    title: Annotated[Optional[str], "New title for the task"] = None,
    description: Annotated[Optional[str], "New description for the task"] = None,
    completed: Annotated[Optional[bool], "New completion status for the task"] = None
) -> dict:
    """
    Modify properties of an existing task for the authenticated user.

    Returns:
    {
      "task_id": "string",
      "status": "updated",
      "title": "string"
    }
    """
    return await tool_update_task(user_id, task_id, title, description, completed)


# Export the server instance
__all__ = ["server"]