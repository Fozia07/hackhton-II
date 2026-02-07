"""
MCP Client Service for the Todo AI Chatbot.
Handles direct database operations for task management.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlmodel import select
from sqlalchemy import insert
from app.models.task import Task, TaskCreate, TaskUpdate
from app.database.session import get_async_session
import uuid


class MCPClientService:
    """
    Service class to handle task operations with direct database access.
    Provides methods for the 5 MCP tools: add, list, complete, delete, update tasks.
    """

    def __init__(self):
        pass

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new task for the user.

        Args:
            user_id: ID of the user adding the task
            title: Title of the task to add
            description: Optional description of the task

        Returns:
            Result with task details or error
        """
        try:
            async for session in get_async_session():
                # Generate values manually to avoid default_factory issues
                task_id = str(uuid.uuid4())
                now = datetime.utcnow()

                # Use SQLAlchemy insert to bypass ORM initialization issues
                stmt = insert(Task).values(
                    id=task_id,
                    user_id=str(user_id),
                    title=title,
                    description=description,
                    completed=False,
                    created_at=now,
                    updated_at=now
                )

                await session.execute(stmt)
                await session.commit()

                # Fetch the created task
                result = await session.execute(
                    select(Task).where(Task.id == task_id)
                )
                new_task = result.scalar_one()

                return {
                    "success": True,
                    "message": f"Task '{title}' added successfully",
                    "task": {
                        "id": new_task.id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "completed": new_task.completed,
                        "created_at": new_task.created_at.isoformat()
                    }
                }
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"[ERROR] Add task failed: {error_detail}")
            return {
                "success": False,
                "error": f"Failed to add task: {str(e)}"
            }

    async def list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """
        List tasks for the user with optional status filter.

        Args:
            user_id: ID of the user listing tasks
            status: Optional status filter (all, pending, completed)

        Returns:
            Result with list of tasks or error
        """
        try:
            async for session in get_async_session():
                # Build query
                statement = select(Task).where(Task.user_id == user_id)

                # Apply status filter if provided
                if status == "pending":
                    statement = statement.where(Task.completed == False)
                elif status == "completed":
                    statement = statement.where(Task.completed == True)
                # "all" or None means no filter

                # Order by creation date (newest first)
                statement = statement.order_by(Task.created_at.desc())

                result = await session.exec(statement)
                tasks = result.all()

                # Convert tasks to dict format
                task_list = [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    for task in tasks
                ]

                return {
                    "success": True,
                    "message": f"Found {len(task_list)} task(s)",
                    "tasks": task_list,
                    "count": len(task_list)
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list tasks: {str(e)}"
            }

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            user_id: ID of the user completing the task
            task_id: ID of the task to complete

        Returns:
            Result with updated task or error
        """
        try:
            async for session in get_async_session():
                # Find the task
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                result = await session.exec(statement)
                task = result.first()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task not found or you don't have permission to complete it"
                    }

                # Mark as completed
                task.completed = True
                task.completed_at = datetime.utcnow()
                task.updated_at = datetime.utcnow()

                session.add(task)
                await session.commit()
                await session.refresh(task)

                return {
                    "success": True,
                    "message": f"Task '{task.title}' marked as completed",
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to complete task: {str(e)}"
            }

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            user_id: ID of the user deleting the task
            task_id: ID of the task to delete

        Returns:
            Result with deletion confirmation or error
        """
        try:
            async for session in get_async_session():
                # Find the task
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                result = await session.exec(statement)
                task = result.first()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task not found or you don't have permission to delete it"
                    }

                # Store task title before deletion
                task_title = task.title

                # Delete the task
                await session.delete(task)
                await session.commit()

                return {
                    "success": True,
                    "message": f"Task '{task_title}' deleted successfully",
                    "deleted_task_id": task_id
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete task: {str(e)}"
            }

    async def update_task(self, user_id: str, task_id: str, title: Optional[str] = None,
                          description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
        """
        Update a task's properties.

        Args:
            user_id: ID of the user updating the task
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            completed: New completion status for the task (optional)

        Returns:
            Result with updated task or error
        """
        try:
            async for session in get_async_session():
                # Find the task
                statement = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                result = await session.exec(statement)
                task = result.first()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task not found or you don't have permission to update it"
                    }

                # Update fields if provided
                updated_fields = []
                if title is not None:
                    task.title = title
                    updated_fields.append("title")
                if description is not None:
                    task.description = description
                    updated_fields.append("description")
                if completed is not None:
                    task.completed = completed
                    updated_fields.append("completed")
                    if completed:
                        task.completed_at = datetime.utcnow()
                    else:
                        task.completed_at = None

                # Update timestamp
                task.updated_at = datetime.utcnow()

                session.add(task)
                await session.commit()
                await session.refresh(task)

                return {
                    "success": True,
                    "message": f"Task '{task.title}' updated successfully",
                    "updated_fields": updated_fields,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "updated_at": task.updated_at.isoformat()
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update task: {str(e)}"
            }


# Global MCP client instance
mcp_client = MCPClientService()