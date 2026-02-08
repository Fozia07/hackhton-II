"""
MCP Tool for completing a task.
Implements the complete_task functionality as specified for the Todo AI Chatbot.
"""
from typing import Dict, Any
from datetime import datetime
from sqlmodel import select

from app.database.session import get_async_session
from app.models import Task
from .base import (
    MCPToolResult,
    validate_user_id,
    validate_task_id
)


async def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a specific task as completed for the authenticated user.

    Args:
        user_id (str): The ID of the user attempting to complete the task
        task_id (str): The ID of the task to mark as completed

    Returns:
        Dict[str, Any]: Result with task_id, status, and title as specified

    Expected Output Format:
    {
      "task_id": "string",
      "status": "completed",
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

    # Use async session to update the task's completion status
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

            # Update the task's completion status
            task.completed = True
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()

            # Save changes to database
            await session.add(task)
            await session.commit()
            await session.refresh(task)

            # Return success response with task ID, status, and title
            return {
                "task_id": task_id,
                "status": "completed",
                "title": task.title
            }

        except Exception as e:
            # Handle any errors during the database operation
            return MCPToolResult(
                success=False,
                error=f"Failed to complete task due to unexpected error: {str(e)}"
            ).to_dict()


# For use with MCP server
def register_complete_task_tool(server):
    """
    Register the complete_task function as an MCP tool with the server.
    """
    @server.tool()
    async def complete_task_tool(user_id: str, task_id: str):
        """
        Mark a specific task as completed for the authenticated user.
        """
        return await complete_task(user_id, task_id)

    return complete_task_tool