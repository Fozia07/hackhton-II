"""
Task model for the console todo application.

This module defines the Task data structure with id, title, and completion status.
"""

class Task:
    """
    Represents a single todo item with id, title, and completion status.
    """

    def __init__(self, task_id: int, title: str, completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Sequential integer identifier starting from 1
            title (str): Non-empty string describing the task
            completed (bool): Boolean indicating if the task is completed (default: False)
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        self.id = task_id
        self.title = title.strip()
        self.completed = completed

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: Formatted string showing task status and title
        """
        status = "x" if self.completed else " "
        return f"[{status}] {self.title}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed representation including ID, title, and status
        """
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary with id, title, and completed status
        """
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }