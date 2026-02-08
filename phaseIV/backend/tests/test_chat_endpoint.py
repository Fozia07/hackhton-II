"""
Tests for the chat endpoint in the Todo AI Chatbot.
Tests for authentication, conversation management, and message persistence.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from sqlmodel import select
from app.database.session import AsyncSession
from app.models import Conversation, Message
from app.main import app
from app.schemas.chat import ChatRequest


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_chat_endpoint_success():
    """Test successful chat request with valid authentication."""
    # Create a mock user ID and token
    user_id = "test_user_123"
    mock_token = "fake_token"

    # Create a test request
    chat_request = ChatRequest(
        message="Test message from user"
    )

    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user_id') as mock_auth:
        mock_auth.return_value = user_id

        with patch('app.services.chat.process_chat_request') as mock_process:
            # Mock the return value of the process function
            mock_conversation = Conversation(
                id="conv_123",
                user_id=user_id,
                title="Test Conversation",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True
            )
            mock_response = "This is a test response"
            mock_process.return_value = (mock_conversation, mock_response)

            # Create a test client
            with TestClient(app) as client:
                # Make a request to the chat endpoint
                response = client.post(
                    f"/api/{user_id}/chat",
                    json=chat_request.model_dump(),
                    headers={"Authorization": f"Bearer {mock_token}"}
                )

                # Assert the response
                assert response.status_code == 200
                assert response.json()["success"] is True
                assert response.json()["conversation_id"] == "conv_123"
                assert "test response" in response.json()["response"]


@pytest.mark.asyncio
async def test_chat_endpoint_with_existing_conversation():
    """Test chat request with an existing conversation ID."""
    user_id = "test_user_123"
    conversation_id = "existing_conv_123"
    mock_token = "fake_token"

    chat_request = ChatRequest(
        conversation_id=conversation_id,
        message="Test message for existing conversation"
    )

    with patch('app.api.deps.get_current_user_id') as mock_auth:
        mock_auth.return_value = user_id

        with patch('app.services.chat.process_chat_request') as mock_process:
            mock_conversation = Conversation(
                id=conversation_id,
                user_id=user_id,
                title="Test Conversation",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True
            )
            mock_response = "Response to existing conversation"
            mock_process.return_value = (mock_conversation, mock_response)

            with TestClient(app) as client:
                response = client.post(
                    f"/api/{user_id}/chat",
                    json=chat_request.model_dump(),
                    headers={"Authorization": f"Bearer {mock_token}"}
                )

                assert response.status_code == 200
                assert response.json()["success"] is True
                assert response.json()["conversation_id"] == conversation_id


@pytest.mark.asyncio
async def test_chat_endpoint_authentication_failure():
    """Test chat request with invalid authentication."""
    user_id = "test_user_123"
    mock_invalid_token = "invalid_token"

    chat_request = ChatRequest(
        message="Test message"
    )

    # Force authentication to fail
    with patch('app.api.deps.get_current_user_id') as mock_auth:
        mock_auth.side_effect = Exception("Invalid token")

        with TestClient(app) as client:
            response = client.post(
                f"/api/{user_id}/chat",
                json=chat_request.model_dump(),
                headers={"Authorization": f"Bearer {mock_invalid_token}"}
            )

            # Should return 401 for unauthorized
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_chat_endpoint_user_id_mismatch():
    """Test chat request where path user_id doesn't match token user_id."""
    path_user_id = "path_user_123"
    token_user_id = "token_user_456"
    mock_token = "fake_token"

    chat_request = ChatRequest(
        message="Test message"
    )

    # Mock the authentication to return a different user ID than in the path
    with patch('app.api.deps.get_current_user_id') as mock_auth:
        mock_auth.return_value = token_user_id  # Different from path_user_id

        with TestClient(app) as client:
            response = client.post(
                f"/api/{path_user_id}/chat",
                json=chat_request.model_dump(),
                headers={"Authorization": f"Bearer {mock_token}"}
            )

            # Should return 403 for forbidden access
            assert response.status_code == 403


def test_health_check():
    """Test the health check endpoint."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test the root endpoint."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to Todo AI Chatbot" in response.json()["message"]


@pytest.mark.asyncio
async def test_save_user_message():
    """Test saving a user message to the database."""
    from app.services.chat import save_user_message

    # Mock the database session
    with patch('app.database.session.get_async_session') as mock_session_gen:
        mock_session = AsyncMock()

        # Mock the result of the query to get the last message
        mock_statement = MagicMock()
        mock_exec_result = AsyncMock()
        mock_last_message = MagicMock()
        mock_last_message.sequence_number = 5

        mock_exec_result.first.return_value = mock_last_message
        mock_session.exec.return_value = mock_exec_result

        mock_add = AsyncMock()
        mock_commit = AsyncMock()
        mock_refresh = AsyncMock()

        mock_session.add = mock_add
        mock_session.commit = mock_commit
        mock_session.refresh = mock_refresh

        # Mock the session generator
        async def mock_session_context():
            yield mock_session

        mock_session_gen.return_value = mock_session_context()

        # Call the function
        result = await save_user_message(
            conversation_id="test_conv",
            user_id="test_user",
            content="Test message content"
        )

        # Assertions
        assert mock_session.add.called
        assert mock_session.commit.called
        assert mock_session.refresh.called
        # The sequence number should be set to the last message's sequence + 1 (6)
        assert result.sequence_number == 6  # This would be set in the actual function


@pytest.mark.asyncio
async def test_create_new_conversation():
    """Test creating a new conversation."""
    from app.services.chat import create_new_conversation

    user_id = "test_user_123"

    # Mock the database session
    with patch('app.database.session.get_async_session') as mock_session_gen:
        mock_session = AsyncMock()

        mock_add = AsyncMock()
        mock_commit = AsyncMock()
        mock_refresh = AsyncMock()

        mock_session.add = mock_add
        mock_session.commit = mock_commit
        mock_session.refresh = mock_refresh

        # Mock the session generator
        async def mock_session_context():
            yield mock_session

        mock_session_gen.return_value = mock_session_context()

        # Call the function
        result = await create_new_conversation(user_id)

        # Assertions
        assert result.user_id == user_id
        assert result.id is not None  # Should be set by the function
        assert result.is_active is True
        assert mock_session.add.called
        assert mock_session.commit.called
        assert mock_session.refresh.called