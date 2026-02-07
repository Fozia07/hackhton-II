"""
API dependencies for the Todo AI Chatbot.
Contains FastAPI dependencies for authentication and other common operations.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError
from app.core.security import verify_access_token, get_user_id_from_token


security = HTTPBearer()


async def get_current_user_id(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Get the current user's ID from the JWT token in the Authorization header.

    Args:
        request: The FastAPI request object
        credentials: The HTTP authorization credentials from the header

    Returns:
        str: The user ID extracted from the JWT token

    Raises:
        HTTPException: If the token is invalid or user ID cannot be extracted
    """
    token = credentials.credentials

    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def verify_user_owns_resource(
    user_id: str,
    path_user_id: str
) -> bool:
    """
    Verify that the authenticated user's ID matches the user ID in the path parameter.

    Args:
        user_id: The user ID from the JWT token (authenticated user)
        path_user_id: The user ID from the path parameter

    Returns:
        bool: True if the user IDs match, raises HTTPException otherwise

    Raises:
        HTTPException: If the user IDs don't match (403 Forbidden)
    """
    if user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't have permission to access this resource"
        )

    return True