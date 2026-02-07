from typing import Optional, List
from sqlmodel import select, Session, func
from sqlalchemy.exc import IntegrityError
from app.models import Task, Conversation, Message, AgentInteraction
from app.models.task import TaskCreate, TaskUpdate
from app.models.conversation import ConversationCreate, ConversationUpdate
from app.models.message import MessageCreate, MessageUpdate
from app.models.agent_interaction import AgentInteractionCreate, AgentInteractionUpdate
from datetime import datetime
import uuid


# Task utility functions
async def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """Create a new task for a user."""
    task = Task.from_orm(task_data)
    task.user_id = user_id
    task.id = str(uuid.uuid4())
    task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    try:
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to create task due to integrity constraint")


async def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def get_tasks_by_user(
    session: Session,
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
        elif status.lower() == "completed":
            statement = statement.where(Task.completed == True)
        # "all" or any other value will return all tasks

    if category:
        statement = statement.where(Task.category == category)

    if priority:
        statement = statement.where(Task.priority == priority)

    result = await session.exec(statement)
    return result.all()


async def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a task for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        return None

    # Update fields
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    if task.completed and task.completed_at is None:
        task.completed_at = datetime.utcnow()
    elif not task.completed:
        task.completed_at = None

    try:
        await session.commit()
        await session.refresh(task)
        return task
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to update task due to integrity constraint")


async def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a task for a user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    task = result.first()

    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


# Conversation utility functions
async def create_conversation(session: Session, conv_data: ConversationCreate, user_id: str) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation.from_orm(conv_data)
    conversation.user_id = user_id
    conversation.id = str(uuid.uuid4())
    conversation.created_at = datetime.utcnow()
    conversation.updated_at = datetime.utcnow()

    try:
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to create conversation due to integrity constraint")


async def get_conversation_by_id(session: Session, conv_id: str, user_id: str) -> Optional[Conversation]:
    """Get a specific conversation by ID for a user."""
    statement = select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
    """Get all conversations for a user."""
    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = await session.exec(statement)
    return result.all()


async def update_conversation(session: Session, conv_id: str, conv_update: ConversationUpdate, user_id: str) -> Optional[Conversation]:
    """Update a conversation for a user."""
    statement = select(Conversation).where(Conversation.id == conv_id, Conversation.user_id == user_id)
    result = await session.exec(statement)
    conversation = result.first()

    if not conversation:
        return None

    # Update fields
    for field, value in conv_update.dict(exclude_unset=True).items():
        setattr(conversation, field, value)

    conversation.updated_at = datetime.utcnow()

    try:
        await session.commit()
        await session.refresh(conversation)
        return conversation
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to update conversation due to integrity constraint")


# Message utility functions
async def create_message(session: Session, msg_data: MessageCreate, user_id: str) -> Message:
    """Create a new message for a user."""
    message = Message.from_orm(msg_data)
    message.user_id = user_id
    message.id = str(uuid.uuid4())
    message.timestamp = datetime.utcnow()

    # Set sequence number if not provided
    if message.sequence_number is None:
        # Get the highest sequence number in the conversation and increment
        statement = select(func.max(Message.sequence_number)).where(Message.conversation_id == message.conversation_id)
        result = await session.exec(statement)
        max_seq = result.one()
        message.sequence_number = 1 if max_seq is None else max_seq + 1

    try:
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to create message due to integrity constraint")


async def get_messages_by_conversation(session: Session, conversation_id: str, user_id: str) -> List[Message]:
    """Get all messages in a conversation for a user."""
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.sequence_number)
    result = await session.exec(statement)
    return result.all()


async def get_message_by_id(session: Session, msg_id: str, user_id: str) -> Optional[Message]:
    """Get a specific message by ID for a user."""
    statement = select(Message).where(Message.id == msg_id, Message.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


# AgentInteraction utility functions
async def create_agent_interaction(session: Session, interaction_data: AgentInteractionCreate, user_id: str) -> AgentInteraction:
    """Create a new agent interaction."""
    interaction = AgentInteraction.from_orm(interaction_data)
    interaction.user_id = user_id
    interaction.id = str(uuid.uuid4())
    interaction.timestamp = datetime.utcnow()

    try:
        session.add(interaction)
        await session.commit()
        await session.refresh(interaction)
        return interaction
    except IntegrityError:
        await session.rollback()
        raise ValueError("Failed to create agent interaction due to integrity constraint")


async def get_agent_interactions_by_message(session: Session, message_id: str, user_id: str) -> List[AgentInteraction]:
    """Get all agent interactions for a specific message."""
    statement = select(AgentInteraction).where(
        AgentInteraction.message_id == message_id,
        AgentInteraction.user_id == user_id
    )
    result = await session.exec(statement)
    return result.all()