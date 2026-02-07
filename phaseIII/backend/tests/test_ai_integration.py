"""
Tests for the AI Integration in the Todo AI Chatbot.
Tests for OpenAI Agent service and MCP client communication.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json
from app.services.ai_agent import AIAgentService
from app.services.mcp_client import MCPClientService, mcp_client
from app.core.config import config


@pytest.mark.asyncio
async def test_mcp_client_add_task():
    """Test the MCP client add_task functionality."""
    with patch('httpx.AsyncClient') as mock_client_class:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "task_id": "test_task_123",
            "status": "created",
            "title": "Test Task"
        }

        # Create a mock client instance
        mock_client_instance = AsyncMock()
        mock_client_instance.request.return_value = mock_response

        # Mock the AsyncClient context manager
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__ = AsyncMock()

        # Create the MCP client service
        client = MCPClientService()

        # Call the add_task method
        result = await client.add_task(
            user_id="test_user_123",
            title="Test Task",
            description="Test Description"
        )

        # Verify the result
        assert result == {
            "task_id": "test_task_123",
            "status": "created",
            "title": "Test Task"
        }

        # Verify the request was made correctly
        mock_client_instance.request.assert_called_once()
        args, kwargs = mock_client_instance.request.call_args
        assert args[0] == "POST"  # method
        assert "/tools/add_task" in kwargs["url"]
        assert kwargs["json"]["user_id"] == "test_user_123"
        assert kwargs["json"]["title"] == "Test Task"


@pytest.mark.asyncio
async def test_mcp_client_list_tasks():
    """Test the MCP client list_tasks functionality."""
    with patch('httpx.AsyncClient') as mock_client_class:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "task_1",
                "title": "Task 1",
                "completed": False
            },
            {
                "id": "task_2",
                "title": "Task 2",
                "completed": True
            }
        ]

        # Create a mock client instance
        mock_client_instance = AsyncMock()
        mock_client_instance.request.return_value = mock_response

        # Mock the AsyncClient context manager
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__ = AsyncMock()

        # Create the MCP client service
        client = MCPClientService()

        # Call the list_tasks method
        result = await client.list_tasks(
            user_id="test_user_123",
            status="all"
        )

        # Verify the result
        assert len(result) == 2
        assert result[0]["id"] == "task_1"
        assert result[1]["id"] == "task_2"

        # Verify the request was made correctly
        mock_client_instance.request.assert_called_once()
        args, kwargs = mock_client_instance.request.call_args
        assert args[0] == "POST"  # method
        assert "/tools/list_tasks" in kwargs["url"]
        assert kwargs["json"]["user_id"] == "test_user_123"
        assert kwargs["json"]["status"] == "all"


@pytest.mark.asyncio
async def test_ai_agent_service_initialization():
    """Test that the AI agent service is initialized correctly."""
    agent_service = AIAgentService()

    # Verify that the service is properly initialized
    assert agent_service.client is not None
    assert agent_service.model == config.openai_model
    assert agent_service.temperature == config.ai_temperature
    assert agent_service.max_tokens == config.ai_max_tokens


@pytest.mark.asyncio
async def test_ai_agent_process_conversation():
    """Test the AI agent's process_conversation functionality with mocked OpenAI."""
    with patch.object(AIAgentService, '_get_conversation_history', return_value=[]) as mock_get_history:
        with patch('openai.AsyncOpenAI') as mock_openai_class:
            # Create mock OpenAI client and response
            mock_client_instance = MagicMock()
            mock_completion = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message = MagicMock()
            mock_choice.message.content = "This is a test response from the AI agent."
            mock_choice.message.tool_calls = None  # No tool calls in this test

            mock_completion.choices = [mock_choice]
            mock_client_instance.chat.completions.create = AsyncMock(return_value=mock_completion)

            mock_openai_class.return_value = mock_client_instance

            # Create the AI agent service
            agent_service = AIAgentService()
            agent_service.client = mock_client_instance

            # Call the process_conversation method
            result = await agent_service.process_conversation(
                user_id="test_user_123",
                conversation_id="test_conv_456",
                user_message="Hello, can you help me create a task?"
            )

            # Verify the result
            assert "test response" in result

            # Verify that the OpenAI API was called
            mock_client_instance.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_ai_agent_with_tool_calls():
    """Test the AI agent's process_conversation functionality when tools are called."""
    with patch.object(AIAgentService, '_get_conversation_history', return_value=[]) as mock_get_history:
        with patch('app.services.mcp_client.mcp_client.add_task') as mock_add_task:
            with patch('openai.AsyncOpenAI') as mock_openai_class:
                # Mock MCP client response
                mock_add_task.return_value = {
                    "task_id": "new_task_123",
                    "status": "created",
                    "title": "Test Task"
                }

                # Create mock OpenAI client and response with tool calls
                mock_client_instance = MagicMock()

                # First call response (with tool call)
                mock_completion1 = MagicMock()
                mock_choice1 = MagicMock()
                mock_choice1.message = MagicMock()
                mock_choice1.message.content = "I'll create that task for you."

                # Create a mock tool call
                mock_tool_call = MagicMock()
                mock_tool_call.function.name = "add_task"
                mock_tool_call.function.arguments = '{"user_id": "test_user_123", "title": "Test Task", "description": "Test Description"}'
                mock_choice1.message.tool_calls = [mock_tool_call]

                mock_completion1.choices = [mock_choice1]

                # Second call response (after tool execution)
                mock_completion2 = MagicMock()
                mock_choice2 = MagicMock()
                mock_choice2.message = MagicMock()
                mock_choice2.message.content = "I've created the task 'Test Task' for you."
                mock_choice2.message.tool_calls = None

                mock_completion2.choices = [mock_choice2]

                # Mock the first call to return the tool call, second call to return the final response
                call_count = 0
                def mock_create(*args, **kwargs):
                    nonlocal call_count
                    call_count += 1
                    if call_count == 1:
                        return mock_completion1
                    else:
                        return mock_completion2

                mock_client_instance.chat.completions.create = AsyncMock(side_effect=mock_create)

                mock_openai_class.return_value = mock_client_instance

                # Create the AI agent service
                agent_service = AIAgentService()
                agent_service.client = mock_client_instance

                # Call the process_conversation method
                result = await agent_service.process_conversation(
                    user_id="test_user_123",
                    conversation_id="test_conv_456",
                    user_message="Please create a task called 'Test Task'"
                )

                # Verify the result includes the tool execution result
                assert "created the task" in result

                # Verify that the MCP client was called
                mock_add_task.assert_called_once_with(
                    user_id="test_user_123",
                    title="Test Task",
                    description="Test Description"
                )


def test_config_loading():
    """Test that the configuration is loaded correctly."""
    # Verify that the config has the expected attributes
    assert hasattr(config, 'openai_api_key')
    assert hasattr(config, 'openai_model')
    assert hasattr(config, 'ai_temperature')
    assert hasattr(config, 'mcp_server_url')
    assert hasattr(config, 'mcp_timeout')


@pytest.mark.asyncio
async def test_mcp_client_error_handling():
    """Test the MCP client's error handling for network failures."""
    with patch('httpx.AsyncClient') as mock_client_class:
        # Create a mock response that simulates an error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        # Create a mock client instance
        mock_client_instance = AsyncMock()
        mock_client_instance.request.return_value = mock_response

        # Mock the AsyncClient context manager
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__ = AsyncMock()

        # Create the MCP client service
        client = MCPClientService()

        # Call the add_task method (which should result in an error)
        result = await client.add_task(
            user_id="test_user_123",
            title="Test Task"
        )

        # Verify the error response
        assert result["success"] is False
        assert "error" in result
        assert "500" in result["error"]


@pytest.mark.asyncio
async def test_mcp_client_timeout_handling():
    """Test the MCP client's error handling for timeout."""
    with patch('httpx.AsyncClient') as mock_client_class:
        # Mock a timeout exception
        mock_client_instance = AsyncMock()
        mock_client_instance.request.side_effect = TimeoutError("Request timed out")

        # Mock the AsyncClient context manager
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__ = AsyncMock()

        # Create the MCP client service
        client = MCPClientService()

        # Call the add_task method (which should result in a timeout error)
        result = await client.add_task(
            user_id="test_user_123",
            title="Test Task"
        )

        # Verify the timeout error response
        assert result["success"] is False
        assert "error" in result
        assert "timed out" in result["error"]