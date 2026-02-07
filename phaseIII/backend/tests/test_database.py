import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task, Conversation, Message, AgentInteraction
from app.database.utils import (
    create_task, get_task_by_id, get_tasks_by_user, update_task, delete_task,
    create_conversation, get_conversation_by_id, update_conversation,
    create_message, get_messages_by_conversation,
    create_agent_interaction
)
from app.models.task import TaskCreate, TaskUpdate
from app.models.conversation import ConversationCreate
from app.models.message import MessageCreate
from app.models.agent_interaction import AgentInteractionCreate
from datetime import datetime


@pytest.mark.asyncio
async def test_create_and_get_task(db_session: AsyncSession):
    """Test creating and retrieving a task."""
    user_id = "test_user_123"

    # Create a task
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="high"
    )
    created_task = await create_task(db_session, task_data, user_id)

    # Verify the task was created
    assert created_task.title == "Test Task"
    assert created_task.user_id == user_id
    assert created_task.completed is False

    # Retrieve the task
    retrieved_task = await get_task_by_id(db_session, created_task.id, user_id)

    # Verify the task was retrieved correctly
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"


@pytest.mark.asyncio
async def test_get_tasks_by_user(db_session: AsyncSession):
    """Test getting all tasks for a user."""
    user_id = "test_user_456"

    # Create multiple tasks
    task_data1 = TaskCreate(title="Task 1", priority="high")
    task_data2 = TaskCreate(title="Task 2", priority="low")

    await create_task(db_session, task_data1, user_id)
    await create_task(db_session, task_data2, user_id)

    # Get all tasks for the user
    tasks = await get_tasks_by_user(db_session, user_id)

    # Verify we got both tasks
    assert len(tasks) == 2
    titles = {task.title for task in tasks}
    assert "Task 1" in titles
    assert "Task 2" in titles


@pytest.mark.asyncio
async def test_update_task(db_session: AsyncSession):
    """Test updating a task."""
    user_id = "test_user_789"

    # Create a task
    task_data = TaskCreate(title="Original Task", priority="medium")
    created_task = await create_task(db_session, task_data, user_id)

    # Update the task
    update_data = TaskUpdate(title="Updated Task", completed=True)
    updated_task = await update_task(db_session, created_task.id, update_data, user_id)

    # Verify the task was updated
    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.completed is True


@pytest.mark.asyncio
async def test_delete_task(db_session: AsyncSession):
    """Test deleting a task."""
    user_id = "test_user_000"

    # Create a task
    task_data = TaskCreate(title="Task to Delete", priority="medium")
    created_task = await create_task(db_session, task_data, user_id)

    # Verify task exists
    retrieved_task = await get_task_by_id(db_session, created_task.id, user_id)
    assert retrieved_task is not None

    # Delete the task
    deletion_result = await delete_task(db_session, created_task.id, user_id)

    # Verify deletion
    assert deletion_result is True
    deleted_task = await get_task_by_id(db_session, created_task.id, user_id)
    assert deleted_task is None


@pytest.mark.asyncio
async def test_create_and_get_conversation(db_session: AsyncSession):
    """Test creating and retrieving a conversation."""
    user_id = "test_user_conv"

    # Create a conversation
    conv_data = ConversationCreate(title="Test Conversation")
    created_conv = await create_conversation(db_session, conv_data, user_id)

    # Verify the conversation was created
    assert created_conv.title == "Test Conversation"
    assert created_conv.user_id == user_id
    assert created_conv.is_active is True

    # Retrieve the conversation
    retrieved_conv = await get_conversation_by_id(db_session, created_conv.id, user_id)

    # Verify the conversation was retrieved correctly
    assert retrieved_conv is not None
    assert retrieved_conv.id == created_conv.id
    assert retrieved_conv.title == "Test Conversation"


@pytest.mark.asyncio
async def test_create_and_get_message(db_session: AsyncSession):
    """Test creating and retrieving messages."""
    user_id = "test_user_msg"

    # Create a conversation first
    conv_data = ConversationCreate(title="Test Conversation for Messages")
    conversation = await create_conversation(db_session, conv_data, user_id)

    # Create a message
    msg_data = MessageCreate(
        conversation_id=conversation.id,
        role="user",
        content="Hello, this is a test message",
        sequence_number=1
    )
    created_msg = await create_message(db_session, msg_data, user_id)

    # Verify the message was created
    assert created_msg.user_id == user_id
    assert created_msg.role == "user"
    assert created_msg.content == "Hello, this is a test message"

    # Get messages by conversation
    messages = await get_messages_by_conversation(db_session, conversation.id, user_id)

    # Verify we got the message
    assert len(messages) == 1
    assert messages[0].id == created_msg.id


@pytest.mark.asyncio
async def test_create_agent_interaction(db_session: AsyncSession):
    """Test creating an agent interaction."""
    user_id = "test_user_agent"

    # Create a message first
    conv_data = ConversationCreate(title="Test Conversation for Agent")
    conversation = await create_conversation(db_session, conv_data, user_id)

    msg_data = MessageCreate(
        conversation_id=conversation.id,
        role="user",
        content="Test message for agent interaction",
        sequence_number=1
    )
    message = await create_message(db_session, msg_data, user_id)

    # Create an agent interaction
    interaction_data = AgentInteractionCreate(
        message_id=message.id,
        tool_name="test_tool",
        tool_input={"param": "value"},
        tool_output={"result": "success"}
    )
    created_interaction = await create_agent_interaction(db_session, interaction_data, user_id)

    # Verify the interaction was created
    assert created_interaction.user_id == user_id
    assert created_interaction.message_id == message.id
    assert created_interaction.tool_name == "test_tool"
    assert created_interaction.tool_input == {"param": "value"}
    assert created_interaction.tool_output == {"result": "success"}
    assert created_interaction.success is True