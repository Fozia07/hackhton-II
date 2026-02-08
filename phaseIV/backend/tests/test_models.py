import pytest
from app.models import Task, Conversation, Message, AgentInteraction
from datetime import datetime
import uuid


def test_task_model():
    """Test Task model creation and attributes."""
    task = Task(
        id=str(uuid.uuid4()),
        user_id="test_user",
        title="Test Task",
        description="Test Description",
        completed=False,
        priority="medium",
        category="test",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    assert task.title == "Test Task"
    assert task.user_id == "test_user"
    assert task.completed is False
    assert task.priority == "medium"
    assert task.category == "test"


def test_conversation_model():
    """Test Conversation model creation and attributes."""
    conversation = Conversation(
        id=str(uuid.uuid4()),
        user_id="test_user",
        title="Test Conversation",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )

    assert conversation.user_id == "test_user"
    assert conversation.title == "Test Conversation"
    assert conversation.is_active is True


def test_message_model():
    """Test Message model creation and attributes."""
    message = Message(
        id=str(uuid.uuid4()),
        conversation_id="test_conv",
        user_id="test_user",
        role="user",
        content="Test message content",
        timestamp=datetime.utcnow(),
        sequence_number=1
    )

    assert message.conversation_id == "test_conv"
    assert message.user_id == "test_user"
    assert message.role == "user"
    assert message.content == "Test message content"
    assert message.sequence_number == 1


def test_agent_interaction_model():
    """Test AgentInteraction model creation and attributes."""
    interaction = AgentInteraction(
        id=str(uuid.uuid4()),
        message_id="test_msg",
        user_id="test_user",
        tool_name="test_tool",
        tool_input={"param": "value"},
        tool_output={"result": "success"},
        timestamp=datetime.utcnow(),
        success=True
    )

    assert interaction.message_id == "test_msg"
    assert interaction.user_id == "test_user"
    assert interaction.tool_name == "test_tool"
    assert interaction.tool_input == {"param": "value"}
    assert interaction.tool_output == {"result": "success"}
    assert interaction.success is True