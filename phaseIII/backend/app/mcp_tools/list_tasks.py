"""
MCP Tool for listing tasks.
Implements the list_tasks functionality as specified for the Todo AI Chatbot.
"""
from typing import Dict, Any, Optional, List
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.database.session import get_async_session
from app.models import Task
from .base import (
    MCPToolResult,
    validate_user_id,
    validate_status
)


async def list_tasks(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all tasks for the authenticated user with optional filtering by status.

    Args:
        user_id (str): The ID of the user whose tasks to retrieve
        status (str, optional): Filter tasks by completion status ("all", "pending", "completed")

    Returns:
        List[Dict[str, Any]]: Array of task objects with all required fields as specified

    Expected Output Format:
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
    # Validate input parameters
    if not validate_user_id(user_id):
        return []

    if status is not None and not validate_status(status):
        return []

    # Build query to select tasks filtered by user_id
    query = select(Task).where(Task.user_id == user_id)

    # Apply additional filter based on status parameter if provided:
    # "pending": filter where completed=False
    # "completed": filter where completed=True
    # "all" or not provided: no additional filter
    if status:
        if status.lower() == "pending":
            query = query.where(Task.completed == False)
        elif status.lower() == "completed":
            query = query.where(Task.completed == True)
        # "all" or any other value will return all tasks (no additional filter)

    # Use async session to execute the query and retrieve matching tasks
    async for session in get_async_session():
        try:
            result = await session.exec(query)
            tasks = result.all()

            # Format results as array of task objects with all required fields
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "priority": getattr(task, 'priority', None),  # Use getattr to handle potential missing attribute
                    "due_date": getattr(task, 'due_date', None),
                    "category": getattr(task, 'category', None),
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                }
                task_list.append(task_dict)

            # Return array of task objects
            return task_list
        except Exception as e:
            # Log the error and return empty array
            print(f"Error retrieving tasks: {str(e)}")
            return []


# For use with MCP server
def register_list_tasks_tool(server):
    """
    Register the list_tasks function as an MCP tool with the server.
    """
    @server.tool()
    async def list_tasks_tool(user_id: str, status: Optional[str] = None):
        """
        Retrieve all tasks for the authenticated user with optional filtering by status.
        """
        return await list_tasks(user_id, status)

    return list_tasks_tool