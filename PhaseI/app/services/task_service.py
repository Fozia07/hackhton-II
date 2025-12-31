"""
Task service for the console todo application.

This module manages the in-memory storage and operations for tasks.
"""
from typing import List, Optional
from app.models.task import Task


class TaskService:
    """
    Service class to manage tasks in memory.
    """

    def __init__(self):
        """
        Initialize the task service with an empty task list and next ID counter.
        """
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str) -> Task:
        """
        Add a new task with the given title.

        Args:
            title (str): The title of the new task

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If the title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(task_id=self.next_id, title=title.strip())
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: List of all tasks
        """
        return self.tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_title: str) -> Optional[Task]:
        """
        Update the title of an existing task.

        Args:
            task_id (int): The ID of the task to update
            new_title (str): The new title for the task

        Returns:
            Optional[Task]: The updated task if found, None otherwise

        Raises:
            ValueError: If the new title is empty
        """
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty")

        task = self.get_task_by_id(task_id)
        if task:
            task.title = new_title.strip()
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id (int): The ID of the task to mark as completed

        Returns:
            bool: True if the task was marked as completed, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            return True
        return False

    def incomplete_task(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark as incomplete

        Returns:
            bool: True if the task was marked as incomplete, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = False
            return True
        return False

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self.next_id