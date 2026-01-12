from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from .config import settings
from datetime import timezone


# Password hashing context with bcrypt and 12 rounds as required
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with 12 rounds.
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user.
    This is a placeholder for future JWT implementation.
    """
    # This will be implemented when actual authentication is added
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with the specified data and expiration.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """
    Verify an access token and return the payload.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Additional security-related utilities will be added here
# when the actual security implementation is developed