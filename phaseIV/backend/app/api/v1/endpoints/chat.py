"""
Chat API endpoint for the Todo AI Chatbot.
Handles chat requests with authentication and AI integration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.api.deps import get_current_user_id, verify_user_owns_resource
from app.services.chat import process_chat_request
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    user=Depends(get_current_user_id)
):
    user_id = user  # JWT se aaya hua user_id
  
    """
    Main chat endpoint that handles user messages and returns AI-generated assistant responses.

    Args:
        user_id: The user ID from the path parameter
        chat_request: The chat request containing the message and optional conversation_id
        authenticated_user_id: The user ID extracted from the JWT token (dependency)

    Returns:
        ChatResponse: Response containing conversation_id, AI-generated assistant response, and other metadata

    Raises:
        HTTPException: If user authentication fails or user IDs don't match
    """

    try:
        # Process the chat request using the AI-integrated service layer
        conversation, assistant_response, tool_calls = await process_chat_request(
            user_id=user_id,
            chat_request=chat_request
        )

        # Return the response with success status
        return ChatResponse(
            success=True,
            conversation_id=conversation.id,
            response=assistant_response,
            tool_calls=tool_calls
        )
    except Exception as e:
        # Return error response if something goes wrong
        return ChatResponse(
            success=False,
            conversation_id=chat_request.conversation_id or "",
            response="",
            error=f"An error occurred while processing your request: {str(e)}",
            tool_calls=[]
        )


# Additional endpoints that might be useful for the frontend
@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """
    Get all conversations for the specified user.

    Args:
        user_id: The user ID from the path parameter
        authenticated_user_id: The user ID extracted from the JWT token (dependency)

    Returns:
        List of conversations for the user
    """
    # Verify that the authenticated user ID matches the user ID in the path
    await verify_user_owns_resource(authenticated_user_id, user_id)

    # TODO: Implement this endpoint to return user's conversations
    # This would require a service function to fetch user's conversations
    return []


@router.get("/{user_id}/conversation/{conversation_id}")
async def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """
    Get all messages for a specific conversation.

    Args:
        user_id: The user ID from the path parameter
        conversation_id: The conversation ID from the path parameter
        authenticated_user_id: The user ID extracted from the JWT token (dependency)

    Returns:
        List of messages in the conversation
    """
    # Verify that the authenticated user ID matches the user ID in the path
    await verify_user_owns_resource(authenticated_user_id, user_id)

    # TODO: Implement this endpoint to return conversation messages
    # This would require a service function to fetch conversation messages
    return []