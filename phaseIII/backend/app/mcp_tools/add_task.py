"""
MCP Tool for adding a new task.
Implements the add_task functionality as specified for the Todo AI Chatbot.
"""
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.database.session import get_async_session
from app.models import Task
from .base import (
    MCPToolResult,
    validate_user_id,
    validate_title,
    validate_description
)


async def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user in the database.

    Args:
        user_id (str): The ID of the user creating the task (for scoping and validation)
        title (str): The title/description of the task to be created
        description (str, optional): Additional details about the task

    Returns:
        Dict[str, Any]: Result with task_id, status, and title as specified

    Expected Output Format:
    {
      "task_id": "string",
      "status": "created",
      "title": "string"
    }
    """
    # Validate input parameters
    if not validate_user_id(user_id):
        return MCPToolResult(
            success=False,
            error="Invalid user_id provided"
        ).to_dict()

    if not validate_title(title):
        return MCPToolResult(
            success=False,
            error="Invalid title provided - title is required and must be 1-255 characters"
        ).to_dict()

    if not validate_description(description):
        return MCPToolResult(
            success=False,
            error="Invalid description provided - must be 1-1000 characters if specified"
        ).to_dict()

    # Create a new Task object using SQLModel
    task_id = str(uuid.uuid4())
    new_task = Task(
        id=task_id,
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Use async session to add the task to the database
    async for session in get_async_session():
        try:
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            # Return success response with the generated task ID, status, and title
            return {
                "task_id": task_id,
                "status": "created",
                "title": title
            }
        except IntegrityError as e:
            await session.rollback()
            return MCPToolResult(
                success=False,
                error=f"Failed to create task due to database integrity error: {str(e)}"
            ).to_dict()
        except Exception as e:
            await session.rollback()
            return MCPToolResult(
                success=False,
                error=f"Failed to create task due to unexpected error: {str(e)}"
            ).to_dict()


# For use with MCP server
def register_add_task_tool(server):
    """
    Register the add_task function as an MCP tool with the server.
    """
    @server.tool()
    async def add_task_tool(user_id: str, title: str, description: Optional[str] = None):
        """
        Create a new task for the authenticated user in the database.
        """
        return await add_task(user_id, title, description)

    return add_task_tool