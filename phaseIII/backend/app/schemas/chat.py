"""
Pydantic models for chat requests and responses in the Todo AI Chatbot.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.

    Attributes:
        conversation_id: Optional ID of existing conversation (creates new if not provided)
        message: User's natural language message
    """
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=1000, description="User's natural language message")


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.

    Attributes:
        success: Whether the operation was successful
        conversation_id: ID of the conversation (newly created or existing)
        response: Assistant's response to the user's message
        tool_calls: List of tool calls made by the assistant (empty for now, will be populated in future steps)
        error: Error message if success is False
    """
    success: bool
    conversation_id: str
    response: str
    tool_calls: List[dict] = []
    error: Optional[str] = None


class MessageResponse(BaseModel):
    """
    Response model for individual messages.

    Attributes:
        id: Message ID
        conversation_id: ID of the conversation
        role: Role of the message sender ('user' or 'assistant')
        content: Content of the message
        timestamp: When the message was created
    """
    id: str
    conversation_id: str
    role: str
    content: str
    timestamp: datetime