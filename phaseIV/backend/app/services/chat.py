"""
Service layer for chat operations in the Todo AI Chatbot.
Handles conversation management, message persistence, and AI agent integration.
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.database.session import get_async_session
from app.models import Conversation, Message
from app.schemas.chat import ChatRequest, MessageResponse
from app.services.ai_agent import ai_agent


async def create_new_conversation(user_id: str, title: Optional[str] = None) -> Conversation:
    """
    Create a new conversation for the user.

    Args:
        user_id: ID of the user creating the conversation
        title: Optional title for the conversation

    Returns:
        Conversation: The newly created conversation object
    """
    conversation = Conversation(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )

    async for session in get_async_session():
        try:
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation
        except IntegrityError:
            await session.rollback()
            raise Exception("Failed to create conversation due to database integrity error")


async def get_conversation_by_id(conversation_id: str, user_id: str) -> Optional[Conversation]:
    """
    Get a conversation by its ID for the specified user.

    Args:
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user who owns the conversation

    Returns:
        Optional[Conversation]: The conversation object if found and owned by user, None otherwise
    """
    async for session in get_async_session():
        try:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            result = await session.exec(statement)
            return result.first()
        except Exception:
            return None


async def save_user_message(conversation_id: str, user_id: str, content: str) -> Message:
    """
    Save a user message to the database.

    Args:
        conversation_id: ID of the conversation the message belongs to
        user_id: ID of the user sending the message
        content: Content of the message

    Returns:
        Message: The saved message object
    """
    message = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=content,
        timestamp=datetime.utcnow(),
        sequence_number=0  # Will be updated in the actual save
    )

    async for session in get_async_session():
        try:
            # First, get the highest sequence number in this conversation to set the proper sequence
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.sequence_number.desc())

            result = await session.exec(statement)
            last_message = result.first()

            if last_message:
                message.sequence_number = last_message.sequence_number + 1
            else:
                message.sequence_number = 1

            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
        except IntegrityError:
            await session.rollback()
            raise Exception("Failed to save user message due to database integrity error")


async def save_assistant_message(conversation_id: str, user_id: str, content: str) -> Message:
    """
    Save an assistant message to the database.

    Args:
        conversation_id: ID of the conversation the message belongs to
        user_id: ID of the user the conversation belongs to
        content: Content of the assistant's message

    Returns:
        Message: The saved message object
    """
    message = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=content,
        timestamp=datetime.utcnow(),
        sequence_number=0  # Will be updated in the actual save
    )

    async for session in get_async_session():
        try:
            # First, get the highest sequence number in this conversation to set the proper sequence
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.sequence_number.desc())

            result = await session.exec(statement)
            last_message = result.first()

            if last_message:
                message.sequence_number = last_message.sequence_number + 1
            else:
                message.sequence_number = 1

            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
        except IntegrityError:
            await session.rollback()
            raise Exception("Failed to save assistant message due to database integrity error")


async def get_conversation_messages(conversation_id: str, user_id: str) -> List[Message]:
    """
    Get all messages for a conversation that belong to the specified user.

    Args:
        conversation_id: ID of the conversation to retrieve messages for
        user_id: ID of the user who owns the conversation

    Returns:
        List[Message]: List of messages in the conversation
    """
    async for session in get_async_session():
        try:
            statement = select(Message).where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            ).order_by(Message.sequence_number)

            result = await session.exec(statement)
            return result.all()
        except Exception:
            return []


async def process_chat_request(user_id: str, chat_request: ChatRequest) -> tuple[Conversation, str, List[Dict[str, Any]]]:
    """
    Process a chat request by creating/resuming conversation and generating AI response.

    Args:
        user_id: ID of the authenticated user
        chat_request: The chat request containing message and optional conversation_id

    Returns:
        tuple[Conversation, str, List[Dict[str, Any]]]: The conversation object, AI-generated response, and tool calls made
    """
    # Get or create conversation
    if chat_request.conversation_id:
        logging.info(f"Attempting to retrieve existing conversation: {chat_request.conversation_id}")
        conversation = await get_conversation_by_id(chat_request.conversation_id, user_id)
        if not conversation:
            # If conversation doesn't exist or doesn't belong to user, create a new one
            logging.info(f"Conversation {chat_request.conversation_id} not found, creating new conversation")
            conversation = await create_new_conversation(user_id)
        else:
            logging.info(f"Continuing existing conversation: {conversation.id}")
    else:
        logging.info("Creating new conversation (no conversation_id provided)")
        conversation = await create_new_conversation(user_id)

    # Save the user's message to the database
    await save_user_message(
        conversation_id=conversation.id,
        user_id=user_id,
        content=chat_request.message
    )

    # Get conversation history for logging
    conversation_history = await get_conversation_messages(conversation.id, user_id)
    logging.info(f"Conversation history length: {len(conversation_history)}")

    # Generate AI response using the AI agent with MCP tools
    try:
        assistant_response, tool_calls = await ai_agent.process_conversation(
            user_id=user_id,
            conversation_id=conversation.id,
            user_message=chat_request.message
        )
        logging.info(f"AI agent response generated successfully with {len(tool_calls)} tool calls")
        logging.info(f"Tool calls: {tool_calls}")
    except Exception as e:
        logging.error(f"AI processing error: {str(e)}")
        # If AI processing fails, return an error message
        assistant_response = f"Sorry, I encountered an error processing your request: {str(e)}. Please try again."
        tool_calls = []

    # Save the assistant's response to the database
    await save_assistant_message(
        conversation_id=conversation.id,
        user_id=user_id,
        content=assistant_response
    )

    # Update conversation's updated_at timestamp
    async for session in get_async_session():
        try:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
        except IntegrityError:
            await session.rollback()

    return conversation, assistant_response, tool_calls

    # Save the assistant's response to the database
    await save_assistant_message(
        conversation_id=conversation.id,
        user_id=user_id,
        content=assistant_response
    )

    # Update conversation's updated_at timestamp
    async for session in get_async_session():
        try:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
        except IntegrityError:
            await session.rollback()

    return conversation, assistant_response