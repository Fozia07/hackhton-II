"""
MCP Tool for deleting a task.
Implements the delete_task functionality as specified for the Todo AI Chatbot.
"""
from typing import Dict, Any
from sqlmodel import select

from app.database.session import get_async_session
from app.models import Task
from .base import (
    MCPToolResult,
    validate_user_id,
    validate_task_id
)


async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Remove a specific task from the user's task list.

    Args:
        user_id (str): The ID of the user attempting to delete the task
        task_id (str): The ID of the task to delete

    Returns:
        Dict[str, Any]: Result with task_id, status, and title as specified

    Expected Output Format:
    {
      "task_id": "string",
      "status": "deleted",
      "title": "string"
    }
    """
    # Validate input parameters
    if not validate_user_id(user_id):
        return MCPToolResult(
            success=False,
            error="Invalid user_id provided"
        ).to_dict()

    if not validate_task_id(task_id):
        return MCPToolResult(
            success=False,
            error="Invalid task_id provided"
        ).to_dict()

    # Use async session to delete the task from the database
    async for session in get_async_session():
        try:
            # Find the task that belongs to the user
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.exec(query)
            task = result.first()

            # Check if the task exists and belongs to the user
            if not task:
                return MCPToolResult(
                    success=False,
                    error="Task not found or does not belong to user"
                ).to_dict()

            # Store the title for the response before deletion
            title = task.title

            # Delete the task record from the database
            await session.delete(task)
            await session.commit()

            # Return success response with original task ID, status, and title
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": title
            }

        except Exception as e:
            # Handle any errors during the database operation
            return MCPToolResult(
                success=False,
                error=f"Failed to delete task due to unexpected error: {str(e)}"
            ).to_dict()


# For use with MCP server
def register_delete_task_tool(server):
    """
    Register the delete_task function as an MCP tool with the server.
    """
    @server.tool()
    async def delete_task_tool(user_id: str, task_id: str):
        """
        Remove a specific task from the user's task list.
        """
        return await delete_task(user_id, task_id)

    return delete_task_tool