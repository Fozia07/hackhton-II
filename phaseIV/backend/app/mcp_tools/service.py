"""
Service layer for MCP tools in the Todo AI Chatbot.
Coordinates all MCP tools with unified error handling and validation.
"""
from typing import Dict, Any, Optional, List
from .add_task import add_task
from .list_tasks import list_tasks
from .complete_task import complete_task
from .delete_task import delete_task
from .update_task import update_task
from .exceptions import ValidationError, AuthorizationError, NotFoundError


class MCPTaskService:
    """
    Service class that coordinates all MCP tools with unified error handling and validation.
    """

    @staticmethod
    async def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task for the authenticated user in the database.

        Args:
            user_id (str): The ID of the user creating the task
            title (str): The title/description of the task to be created
            description (str, optional): Additional details about the task

        Returns:
            Dict[str, Any]: Result with task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
                raise ValidationError("Invalid user_id provided")

            if not title or not isinstance(title, str) or len(title.strip()) == 0 or len(title) > 255:
                raise ValidationError("Invalid title provided - title is required and must be 1-255 characters")

            if description is not None and (not isinstance(description, str) or len(description) > 1000):
                raise ValidationError("Invalid description provided - must be 1-1000 characters if specified")

            # Call the underlying tool function
            result = await add_task(user_id, title, description)

            return result
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to add task: {str(e)}")

    @staticmethod
    async def list_tasks(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks for the authenticated user with optional filtering by status.

        Args:
            user_id (str): The ID of the user whose tasks to retrieve
            status (str, optional): Filter tasks by completion status ("all", "pending", "completed")

        Returns:
            List[Dict[str, Any]]: Array of task objects with all required fields
        """
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
                raise ValidationError("Invalid user_id provided")

            if status is not None and status.lower() not in ["all", "pending", "completed"]:
                raise ValidationError("Invalid status provided - must be one of 'all', 'pending', 'completed'")

            # Call the underlying tool function
            result = await list_tasks(user_id, status)

            return result
        except ValidationError:
            raise
        except Exception as e:
            raise Exception(f"Failed to list tasks: {str(e)}")

    @staticmethod
    async def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Mark a specific task as completed for the authenticated user.

        Args:
            user_id (str): The ID of the user attempting to complete the task
            task_id (str): The ID of the task to mark as completed

        Returns:
            Dict[str, Any]: Result with task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
                raise ValidationError("Invalid user_id provided")

            if not task_id or not isinstance(task_id, str) or len(task_id.strip()) == 0:
                raise ValidationError("Invalid task_id provided")

            # Call the underlying tool function
            result = await complete_task(user_id, task_id)

            # Check if the result indicates an error
            if not result.get("status") or result.get("status") == "error":
                raise NotFoundError(result.get("error", "Task not found or does not belong to user"))

            return result
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to complete task: {str(e)}")

    @staticmethod
    async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Remove a specific task from the user's task list.

        Args:
            user_id (str): The ID of the user attempting to delete the task
            task_id (str): The ID of the task to delete

        Returns:
            Dict[str, Any]: Result with task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
                raise ValidationError("Invalid user_id provided")

            if not task_id or not isinstance(task_id, str) or len(task_id.strip()) == 0:
                raise ValidationError("Invalid task_id provided")

            # Call the underlying tool function
            result = await delete_task(user_id, task_id)

            # Check if the result indicates an error
            if not result.get("status") or result.get("status") == "error":
                raise NotFoundError(result.get("error", "Task not found or does not belong to user"))

            return result
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to delete task: {str(e)}")

    @staticmethod
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
            Dict[str, Any]: Result with task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
                raise ValidationError("Invalid user_id provided")

            if not task_id or not isinstance(task_id, str) or len(task_id.strip()) == 0:
                raise ValidationError("Invalid task_id provided")

            if title is not None and (not isinstance(title, str) or len(title.strip()) == 0 or len(title) > 255):
                raise ValidationError("Invalid title provided - title must be 1-255 characters")

            if description is not None and (not isinstance(description, str) or len(description) > 1000):
                raise ValidationError("Invalid description provided - must be 1-1000 characters if specified")

            if completed is not None and not isinstance(completed, bool):
                raise ValidationError("Invalid completed status provided - must be a boolean value")

            # Call the underlying tool function
            result = await update_task(user_id, task_id, title, description, completed)

            # Check if the result indicates an error
            if not result.get("status") or result.get("status") == "error":
                raise NotFoundError(result.get("error", "Task not found or does not belong to user"))

            return result
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to update task: {str(e)}")


# Create an instance of the service for convenience
task_service = MCPTaskService()