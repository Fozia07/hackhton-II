"""
MCP Tool for updating a task.
Implements the update_task functionality as specified for the Todo AI Chatbot.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlmodel import select

from app.database.session import get_async_session
from app.models import Task
from .base import (
    MCPToolResult,
    validate_user_id,
    validate_task_id,
    validate_title,
    validate_description,
    validate_priority
)


async def update_task(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Modify properties of an existing task for the authenticated user.

    Args:
        user_id (str): The ID of the user attempting to update the task
        task_id (str): The ID of the task to update
        title (str, optional): New title for the task
        description (str, optional): New description for the task
        completed (bool, optional): New completion status for the task

    Returns:
        Dict[str, Any]: Result with task_id, status, and title as specified

    Expected Output Format:
    {
      "task_id": "string",
      "status": "updated",
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

    if title is not None and not validate_title(title):
        return MCPToolResult(
            success=False,
            error="Invalid title provided - title must be 1-255 characters"
        ).to_dict()

    if description is not None and not validate_description(description):
        return MCPToolResult(
            success=False,
            error="Invalid description provided - must be 1-1000 characters if specified"
        ).to_dict()

    if completed is not None and not isinstance(completed, bool):
        return MCPToolResult(
            success=False,
            error="Invalid completed status provided - must be a boolean value"
        ).to_dict()

    # Use async session to update the task in the database
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

            # Update fields if provided in input
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed
                # If completed status is changing to true and completed_at is not set, set it to current time
                if completed and task.completed_at is None:
                    task.completed_at = datetime.utcnow()
                # If completed status is changing to false, set completed_at to null
                elif not completed:
                    task.completed_at = None

            # Update the updated_at timestamp to current time
            task.updated_at = datetime.utcnow()

            # Save changes to database
            await session.add(task)
            await session.commit()
            await session.refresh(task)

            # Return success response with task ID, status, and updated title
            return {
                "task_id": task_id,
                "status": "updated",
                "title": task.title
            }

        except Exception as e:
            # Handle any errors during the database operation
            return MCPToolResult(
                success=False,
                error=f"Failed to update task due to unexpected error: {str(e)}"
            ).to_dict()


# For use with MCP server
def register_update_task_tool(server):
    """
    Register the update_task function as an MCP tool with the server.
    """
    @server.tool()
    async def update_task_tool(user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        """
        Modify properties of an existing task for the authenticated user.
        """
        return await update_task(user_id, task_id, title, description, completed)

    return update_task_tool