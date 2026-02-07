"""
Tests for the MCP tools service layer in the Todo AI Chatbot.
Tests for the service layer coordinating all tools.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.mcp_tools.service import MCPTaskService
from app.mcp_tools.exceptions import ValidationError, NotFoundError


@pytest.mark.asyncio
async def test_add_task_service_success():
    """Test successful addition of a task via the service."""
    user_id = "test_user_123"
    title = "Test Task"
    description = "Test Description"

    with patch('app.mcp_tools.service.add_task') as mock_add_task:
        expected_result = {
            "task_id": "task_123",
            "status": "created",
            "title": title
        }
        mock_add_task.return_value = expected_result

        result = await MCPTaskService.add_task(user_id, title, description)

        # Verify the result
        assert result == expected_result
        mock_add_task.assert_called_once_with(user_id, title, description)


@pytest.mark.asyncio
async def test_add_task_service_validation_error():
    """Test add_task service with validation error."""
    user_id = ""  # Invalid user_id
    title = "Test Task"
    description = "Test Description"

    with pytest.raises(ValidationError):
        await MCPTaskService.add_task(user_id, title, description)


@pytest.mark.asyncio
async def test_list_tasks_service_success():
    """Test successful listing of tasks via the service."""
    user_id = "test_user_123"
    status = "all"

    expected_result = [
        {
            "id": "task_123",
            "title": "Test Task",
            "completed": False,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "completed_at": None
        }
    ]

    with patch('app.mcp_tools.service.list_tasks') as mock_list_tasks:
        mock_list_tasks.return_value = expected_result

        result = await MCPTaskService.list_tasks(user_id, status)

        # Verify the result
        assert result == expected_result
        mock_list_tasks.assert_called_once_with(user_id, status)


@pytest.mark.asyncio
async def test_list_tasks_service_validation_error():
    """Test list_tasks service with validation error."""
    user_id = "test_user_123"
    status = "invalid_status"  # Invalid status

    with pytest.raises(ValidationError):
        await MCPTaskService.list_tasks(user_id, status)


@pytest.mark.asyncio
async def test_complete_task_service_success():
    """Test successful completion of a task via the service."""
    user_id = "test_user_123"
    task_id = "task_123"

    expected_result = {
        "task_id": task_id,
        "status": "completed",
        "title": "Test Task"
    }

    with patch('app.mcp_tools.service.complete_task') as mock_complete_task:
        mock_complete_task.return_value = expected_result

        result = await MCPTaskService.complete_task(user_id, task_id)

        # Verify the result
        assert result == expected_result
        mock_complete_task.assert_called_once_with(user_id, task_id)


@pytest.mark.asyncio
async def test_complete_task_service_not_found():
    """Test complete_task service with task not found."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"

    with patch('app.mcp_tools.service.complete_task') as mock_complete_task:
        error_result = {"status": "error", "error": "Task not found"}
        mock_complete_task.return_value = error_result

        with pytest.raises(NotFoundError):
            await MCPTaskService.complete_task(user_id, task_id)


@pytest.mark.asyncio
async def test_delete_task_service_success():
    """Test successful deletion of a task via the service."""
    user_id = "test_user_123"
    task_id = "task_123"

    expected_result = {
        "task_id": task_id,
        "status": "deleted",
        "title": "Test Task"
    }

    with patch('app.mcp_tools.service.delete_task') as mock_delete_task:
        mock_delete_task.return_value = expected_result

        result = await MCPTaskService.delete_task(user_id, task_id)

        # Verify the result
        assert result == expected_result
        mock_delete_task.assert_called_once_with(user_id, task_id)


@pytest.mark.asyncio
async def test_delete_task_service_not_found():
    """Test delete_task service with task not found."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"

    with patch('app.mcp_tools.service.delete_task') as mock_delete_task:
        error_result = {"status": "error", "error": "Task not found"}
        mock_delete_task.return_value = error_result

        with pytest.raises(NotFoundError):
            await MCPTaskService.delete_task(user_id, task_id)


@pytest.mark.asyncio
async def test_update_task_service_success():
    """Test successful update of a task via the service."""
    user_id = "test_user_123"
    task_id = "task_123"
    new_title = "Updated Task"

    expected_result = {
        "task_id": task_id,
        "status": "updated",
        "title": new_title
    }

    with patch('app.mcp_tools.service.update_task') as mock_update_task:
        mock_update_task.return_value = expected_result

        result = await MCPTaskService.update_task(user_id, task_id, title=new_title)

        # Verify the result
        assert result == expected_result
        mock_update_task.assert_called_once_with(user_id, task_id, title=new_title, description=None, completed=None)


@pytest.mark.asyncio
async def test_update_task_service_validation_error():
    """Test update_task service with validation error."""
    user_id = "test_user_123"
    task_id = "task_123"
    invalid_completed = "not_a_boolean"  # Invalid type

    with pytest.raises(ValidationError):
        await MCPTaskService.update_task(user_id, task_id, completed=invalid_completed)


@pytest.mark.asyncio
async def test_update_task_service_not_found():
    """Test update_task service with task not found."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"
    new_title = "Updated Task"

    with patch('app.mcp_tools.service.update_task') as mock_update_task:
        error_result = {"status": "error", "error": "Task not found"}
        mock_update_task.return_value = error_result

        with pytest.raises(NotFoundError):
            await MCPTaskService.update_task(user_id, task_id, title=new_title)