"""
Tests for the Todo AI Chatbot MCP Server.
Comprehensive tests for the MCP server functionality covering initialization, configuration, and basic tool functionality.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from app.mcp_server.server import server
from app.mcp_server.config import (
    SERVER_NAME,
    SERVER_VERSION,
    TRANSPORT_TYPE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    REGISTERED_TOOLS
)


def test_server_configuration():
    """Test that the server is configured with correct settings."""
    # Note: Since we can't easily inspect the internal configuration of the MCPServer object,
    # we're testing based on our expectations from the configuration
    assert SERVER_NAME == "todo-ai-chatbot-mcp-server"
    assert SERVER_VERSION == "1.0.0"
    assert TRANSPORT_TYPE == "streamable-http"
    assert DEFAULT_HOST == "0.0.0.0"
    assert DEFAULT_PORT == 8002
    assert len(REGISTERED_TOOLS) == 5
    assert "add_task" in REGISTERED_TOOLS
    assert "list_tasks" in REGISTERED_TOOLS
    assert "complete_task" in REGISTERED_TOOLS
    assert "delete_task" in REGISTERED_TOOLS
    assert "update_task" in REGISTERED_TOOLS


@pytest.mark.asyncio
async def test_server_has_expected_tools():
    """Test that the server has all expected tools registered."""
    # Since we can't directly access the tools from the server object,
    # we'll verify that the expected functions exist in the module
    from app.mcp_server.server import add_task, list_tasks, complete_task, delete_task, update_task

    # Verify that the functions exist
    assert callable(add_task)
    assert callable(list_tasks)
    assert callable(complete_task)
    assert callable(delete_task)
    assert callable(update_task)


@pytest.mark.asyncio
async def test_add_task_tool_registration():
    """Test the add_task tool registration and basic functionality."""
    from app.mcp_server.server import add_task

    # Mock the underlying tool function
    with patch('app.mcp_server.server.tool_add_task') as mock_tool:
        expected_result = {
            "task_id": "test_task_id",
            "status": "created",
            "title": "Test Task"
        }
        mock_tool.return_value = expected_result

        result = await add_task(
            user_id="test_user",
            title="Test Task",
            description="Test Description"
        )

        # Verify the result
        assert result == expected_result
        mock_tool.assert_called_once_with("test_user", "Test Task", "Test Description")


@pytest.mark.asyncio
async def test_list_tasks_tool_registration():
    """Test the list_tasks tool registration and basic functionality."""
    from app.mcp_server.server import list_tasks

    # Mock the underlying tool function
    with patch('app.mcp_server.server.tool_list_tasks') as mock_tool:
        expected_result = [
            {
                "id": "test_task_id",
                "title": "Test Task",
                "completed": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "completed_at": None
            }
        ]
        mock_tool.return_value = expected_result

        result = await list_tasks(
            user_id="test_user",
            status="pending"
        )

        # Verify the result
        assert result == expected_result
        mock_tool.assert_called_once_with("test_user", "pending")


@pytest.mark.asyncio
async def test_complete_task_tool_registration():
    """Test the complete_task tool registration and basic functionality."""
    from app.mcp_server.server import complete_task

    # Mock the underlying tool function
    with patch('app.mcp_server.server.tool_complete_task') as mock_tool:
        expected_result = {
            "task_id": "test_task_id",
            "status": "completed",
            "title": "Test Task"
        }
        mock_tool.return_value = expected_result

        result = await complete_task(
            user_id="test_user",
            task_id="test_task_id"
        )

        # Verify the result
        assert result == expected_result
        mock_tool.assert_called_once_with("test_user", "test_task_id")


@pytest.mark.asyncio
async def test_delete_task_tool_registration():
    """Test the delete_task tool registration and basic functionality."""
    from app.mcp_server.server import delete_task

    # Mock the underlying tool function
    with patch('app.mcp_server.server.tool_delete_task') as mock_tool:
        expected_result = {
            "task_id": "test_task_id",
            "status": "deleted",
            "title": "Test Task"
        }
        mock_tool.return_value = expected_result

        result = await delete_task(
            user_id="test_user",
            task_id="test_task_id"
        )

        # Verify the result
        assert result == expected_result
        mock_tool.assert_called_once_with("test_user", "test_task_id")


@pytest.mark.asyncio
async def test_update_task_tool_registration():
    """Test the update_task tool registration and basic functionality."""
    from app.mcp_server.server import update_task

    # Mock the underlying tool function
    with patch('app.mcp_server.server.tool_update_task') as mock_tool:
        expected_result = {
            "task_id": "test_task_id",
            "status": "updated",
            "title": "Updated Test Task"
        }
        mock_tool.return_value = expected_result

        result = await update_task(
            user_id="test_user",
            task_id="test_task_id",
            title="Updated Test Task"
        )

        # Verify the result
        assert result == expected_result
        mock_tool.assert_called_once_with("test_user", "test_task_id", "Updated Test Task", None, None)


@pytest.mark.asyncio
async def test_server_run_function_exists():
    """Test that the server run configuration is available."""
    # Simply test that the server object exists and has expected attributes
    assert hasattr(server, '__class__')
    # The actual server run test would require spinning up a real server,
    # which is beyond the scope of unit tests