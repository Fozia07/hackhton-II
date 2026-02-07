"""
Base classes and utilities for MCP tools in the Todo AI Chatbot.
This module provides common functionality and base classes for all MCP tools.
"""
from typing import Any, Dict, Optional, Protocol
from abc import ABC, abstractmethod
from datetime import datetime
import json


class MCPToolResult:
    """
    Represents the result of an MCP tool execution.
    """
    def __init__(self, success: bool, data: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        self.success = success
        self.data = data or {}
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary for JSON serialization."""
        result = {
            "success": self.success
        }
        if self.success:
            result.update(self.data)
        else:
            result["error"] = self.error
        return result


class DatabaseOperation(Protocol):
    """
    Protocol defining the interface for database operations that MCP tools can use.
    """
    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        ...

    async def list_tasks(self, user_id: str, status: Optional[str] = None) -> list:
        ...

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        ...

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        ...

    async def update_task(self, user_id: str, task_id: str, **updates) -> Dict[str, Any]:
        ...


def validate_user_id(user_id: str) -> bool:
    """
    Validate that the user_id is properly formatted.
    In a real implementation, this might check against a user database.
    """
    if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
        return False
    return True


def validate_task_id(task_id: str) -> bool:
    """
    Validate that the task_id is properly formatted.
    """
    if not task_id or not isinstance(task_id, str) or len(task_id.strip()) == 0:
        return False
    return True


def validate_title(title: str) -> bool:
    """
    Validate that the title meets requirements.
    """
    if not title or not isinstance(title, str):
        return False
    if len(title.strip()) == 0 or len(title) > 255:
        return False
    return True


def validate_description(description: Optional[str]) -> bool:
    """
    Validate that the description meets requirements.
    """
    if description is None:
        return True
    if not isinstance(description, str) or len(description) > 1000:
        return False
    return True


def validate_status(status: Optional[str]) -> bool:
    """
    Validate that the status is one of the allowed values.
    """
    if status is None:
        return True
    if status.lower() not in ["all", "pending", "completed"]:
        return False
    return True


def validate_priority(priority: Optional[str]) -> bool:
    """
    Validate that the priority is one of the allowed values.
    """
    if priority is None:
        return True
    if priority.lower() not in ["low", "medium", "high"]:
        return False
    return True