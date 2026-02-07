"""
Tests for MCP tools in the Todo AI Chatbot.
Comprehensive tests for all MCP tools covering normal operations and edge cases.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.mcp_tools.add_task import add_task
from app.mcp_tools.list_tasks import list_tasks
from app.mcp_tools.complete_task import complete_task
from app.mcp_tools.delete_task import delete_task
from app.mcp_tools.update_task import update_task
from app.models import Task
from datetime import datetime


@pytest.mark.asyncio
async def test_add_task_success():
    """Test successful addition of a task."""
    user_id = "test_user_123"
    title = "Test Task"
    description = "Test Description"

    with patch('app.mcp_tools.add_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_add = AsyncMock()
        mock_commit = AsyncMock()
        mock_refresh = AsyncMock()

        mock_session.add = mock_add
        mock_session.commit = mock_commit
        mock_session.refresh = mock_refresh

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await add_task(user_id, title, description)

        # Verify the result format
        assert "task_id" in result
        assert result["status"] == "created"
        assert result["title"] == title

        # Verify the session methods were called
        mock_add.assert_called_once()
        mock_commit.assert_called_once()


@pytest.mark.asyncio
async def test_add_task_missing_title():
    """Test add_task with missing title."""
    user_id = "test_user_123"
    title = ""
    description = "Test Description"

    result = await add_task(user_id, title, description)

    # Verify error response
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_add_task_invalid_user_id():
    """Test add_task with invalid user_id."""
    user_id = ""
    title = "Test Task"
    description = "Test Description"

    result = await add_task(user_id, title, description)

    # Verify error response
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_list_tasks_success():
    """Test successful listing of tasks."""
    user_id = "test_user_123"
    status = "all"

    # Create mock tasks
    mock_task = MagicMock()
    mock_task.id = "task_123"
    mock_task.title = "Test Task"
    mock_task.completed = False
    mock_task.created_at = datetime.utcnow()
    mock_task.updated_at = datetime.utcnow()
    mock_task.completed_at = None

    with patch('app.mcp_tools.list_tasks.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return the mock tasks
        mock_exec_result = AsyncMock()
        mock_exec_result.all.return_value = [mock_task]
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await list_tasks(user_id, status)

        # Verify the result format
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == "task_123"
        assert result[0]["title"] == "Test Task"


@pytest.mark.asyncio
async def test_list_tasks_empty_result():
    """Test list_tasks with no tasks found."""
    user_id = "test_user_123"
    status = "pending"

    with patch('app.mcp_tools.list_tasks.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return empty list
        mock_exec_result = AsyncMock()
        mock_exec_result.all.return_value = []
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await list_tasks(user_id, status)

        # Verify the result is an empty list
        assert result == []


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test successful completion of a task."""
    user_id = "test_user_123"
    task_id = "task_123"

    # Create mock task
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.title = "Test Task"
    mock_task.completed = False
    mock_task.completed_at = None
    mock_task.updated_at = datetime.utcnow()

    with patch('app.mcp_tools.complete_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return the mock task
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        mock_add = AsyncMock()
        mock_commit = AsyncMock()
        mock_refresh = AsyncMock()
        mock_session.add = mock_add
        mock_session.commit = mock_commit
        mock_session.refresh = mock_refresh

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await complete_task(user_id, task_id)

        # Verify the result format
        assert result["task_id"] == task_id
        assert result["status"] == "completed"
        assert result["title"] == "Test Task"

        # Verify the task properties were updated
        assert mock_task.completed is True
        assert mock_task.completed_at is not None


@pytest.mark.asyncio
async def test_complete_task_not_found():
    """Test complete_task when task doesn't exist."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"

    with patch('app.mcp_tools.complete_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return None (task not found)
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = None
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await complete_task(user_id, task_id)

        # Verify error response
        assert result["success"] is False
        assert "error" in result


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test successful deletion of a task."""
    user_id = "test_user_123"
    task_id = "task_123"

    # Create mock task
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.title = "Test Task"

    with patch('app.mcp_tools.delete_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return the mock task
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        mock_delete = AsyncMock()
        mock_commit = AsyncMock()
        mock_session.delete = mock_delete
        mock_session.commit = mock_commit

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await delete_task(user_id, task_id)

        # Verify the result format
        assert result["task_id"] == task_id
        assert result["status"] == "deleted"
        assert result["title"] == "Test Task"

        # Verify the delete method was called
        mock_delete.assert_called_once_with(mock_task)
        mock_commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """Test delete_task when task doesn't exist."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"

    with patch('app.mcp_tools.delete_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return None (task not found)
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = None
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await delete_task(user_id, task_id)

        # Verify error response
        assert result["success"] is False
        assert "error" in result


@pytest.mark.asyncio
async def test_update_task_success():
    """Test successful update of a task."""
    user_id = "test_user_123"
    task_id = "task_123"
    new_title = "Updated Task"

    # Create mock task
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.title = "Original Task"
    mock_task.description = "Original Description"
    mock_task.completed = False
    mock_task.updated_at = datetime.utcnow()

    with patch('app.mcp_tools.update_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return the mock task
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        mock_add = AsyncMock()
        mock_commit = AsyncMock()
        mock_refresh = AsyncMock()
        mock_session.add = mock_add
        mock_session.commit = mock_commit
        mock_session.refresh = mock_refresh

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await update_task(user_id, task_id, title=new_title)

        # Verify the result format
        assert result["task_id"] == task_id
        assert result["status"] == "updated"
        assert result["title"] == new_title

        # Verify the task properties were updated
        assert mock_task.title == new_title


@pytest.mark.asyncio
async def test_update_task_not_found():
    """Test update_task when task doesn't exist."""
    user_id = "test_user_123"
    task_id = "nonexistent_task"
    new_title = "Updated Task"

    with patch('app.mcp_tools.update_task.get_async_session') as mock_get_session:
        mock_session = AsyncMock()

        # Mock the exec method to return None (task not found)
        mock_exec_result = AsyncMock()
        mock_exec_result.first.return_value = None
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Mock the async session context manager
        async def mock_session_context():
            yield mock_session

        mock_get_session.return_value = mock_session_context()

        result = await update_task(user_id, task_id, title=new_title)

        # Verify error response
        assert result["success"] is False
        assert "error" in result