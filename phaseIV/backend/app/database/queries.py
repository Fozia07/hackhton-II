from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task, Conversation, Message, AgentInteraction
from app.models.task import TaskCreate, TaskUpdate
from app.models.conversation import ConversationCreate, ConversationUpdate
from app.models.message import MessageCreate, MessageUpdate
from app.models.agent_interaction import AgentInteractionCreate, AgentInteractionUpdate
from datetime import datetime
import uuid


# Task queries
async def create_task_query(session: AsyncSession, task_data: TaskCreate, user_id: str) -> Task:
    """Create a new task for a user."""
    task = Task.model_validate(task_data)
    task.user_id = user_id
    task.id = str(uuid.uuid4())
    task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task_by_id_query(session: AsyncSession, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def get_tasks_by_user_query(
    session: AsyncSession,
    user_id: str,
    status: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None
) -> List[Task]:
    """Get all tasks for a user with optional filtering."""
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        if status.lower() == "pending":
            statement = statement.where(Task.completed == False)
        elif status.lower == "completed":
            statement = statement.where(Task.completed == True)

    if category:
        statement = statement.where(Task.category == category)

    if priority:
        statement = statement.where(Task.priority == priority)

    result = await session.exec(statement)
    return result.all()


async def update_task_query(session: AsyncSession, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a task for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        return None

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    if task.completed and task.completed_at is None:
        task.completed_at = datetime.utcnow()
    elif not task.completed:
        task.completed_at = None

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task_query(session: AsyncSession, task_id: str, user_id: str) -> bool:
    """Delete a task for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


# Conversation queries
async def create_conversation_query(session: AsyncSession, conv_data: ConversationCreate, user_id: str) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation.model_validate(conv_data)
    conversation.user_id = user_id
    conversation.id = str(uuid.uuid4())
    conversation.created_at = datetime.utcnow()
    conversation.updated_at = datetime.utcnow()

    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation_by_id_query(session: AsyncSession, conv_id: str, user_id: str) -> Optional[Conversation]:
    """Get a specific conversation by ID for a user."""
    statement = select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def get_conversations_by_user_query(session: AsyncSession, user_id: str) -> List[Conversation]:
    """Get all conversations for a user."""
    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = await session.exec(statement)
    return result.all()


async def update_conversation_query(session: AsyncSession, conv_id: str, conv_update: ConversationUpdate, user_id: str) -> Optional[Conversation]:
    """Update a conversation for a user."""
    statement = select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user_id)
    result = await session.exec(statement)
    conversation = result.first()

    if not conversation:
        return None

    # Update fields
    update_data = conv_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)

    conversation.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(conversation)
    return conversation


# Message queries
async def create_message_query(session: AsyncSession, msg_data: MessageCreate, user_id: str) -> Message:
    """Create a new message for a user."""
    message = Message.model_validate(msg_data)
    message.user_id = user_id
    message.id = str(uuid.uuid4())
    message.timestamp = datetime.utcnow()

    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def get_messages_by_conversation_query(session: AsyncSession, conversation_id: str, user_id: str) -> List[Message]:
    """Get all messages in a conversation for a user."""
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.sequence_number)
    result = await session.exec(statement)
    return result.all()


async def get_message_by_id_query(session: AsyncSession, msg_id: str, user_id: str) -> Optional[Message]:
    """Get a specific message by ID for a user."""
    statement = select(Message).where(Message.id == msg_id, Message.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


# AgentInteraction queries
async def create_agent_interaction_query(session: AsyncSession, interaction_data: AgentInteractionCreate, user_id: str) -> AgentInteraction:
    """Create a new agent interaction."""
    interaction = AgentInteraction.model_validate(interaction_data)
    interaction.user_id = user_id
    interaction.id = str(uuid.uuid4())
    interaction.timestamp = datetime.utcnow()

    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)
    return interaction


async def get_agent_interactions_by_message_query(session: AsyncSession, message_id: str, user_id: str) -> List[AgentInteraction]:
    """Get all agent interactions for a specific message."""
    statement = select(AgentInteraction).where(
        AgentInteraction.message_id == message_id,
        AgentInteraction.user_id == user_id
    )
    result = await session.exec(statement)
    return result.all()