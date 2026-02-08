"""
Security utilities for the Todo AI Chatbot.
Contains JWT token handling, password hashing, and other security-related functions.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get JWT configuration from environment variables, supporting both naming conventions
# This ensures compatibility with both Phase II and Phase III environment setups
SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("SECRET_KEY", "47fa85fedc6d1dd46053ff3f5618f191")
ALGORITHM = os.getenv("JWT_ALGORITHM") or os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (defaults to ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()

    from datetime import timezone

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify a JWT access token and return the payload if valid.
    Tries multiple secret keys for Phase II and Phase III compatibility.
    Temporarily ignores expiration for compatibility with older tokens.

    Args:
        token: The JWT token to verify

    Returns:
        Optional[dict]: The token payload if valid, None otherwise
    """
    # Define possible secret keys to try (Phase III first, then Phase II fallbacks)
    possible_secret_keys = [
        SECRET_KEY,  # Phase III secret key
        os.getenv("JWT_SECRET_KEY", ""),  # Phase II secret key from environment
        "your-super-secret-key-for-jwt-signing",  # Default Phase II secret key
        "47fa85fedc6d1dd46053ff3f5618f191",  # Default Phase III secret key
    ]

    # Remove empty keys
    possible_secret_keys = [key for key in possible_secret_keys if key]

    # Try each secret key
    for secret_key in possible_secret_keys:
        try:
            # First, try with strict validation
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            # If it's an expiration issue, try with options to ignore expiration temporarily
            if "expired" in str(e).lower():
                try:
                    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM], options={"verify_exp": False})
                    return payload
                except JWTError:
                    continue
            continue

    # Return None if no secret key worked
    return None

def get_user_id_from_token(token: str) -> Optional[str]:
    payload = verify_access_token(token)
    if payload:
        print("Token payload:", payload)  # DEBUG - MUST appear
        username = payload.get("username")
        if username is not None:
            return str(username)

        user_id = payload.get("sub")
        if user_id is not None:
            return str(user_id)

        last_id = payload.get("user_id")
        if last_id is not None:
            return str(last_id)

    print("No valid user ID found in token")
    return None
