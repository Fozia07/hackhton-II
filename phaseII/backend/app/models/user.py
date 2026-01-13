from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator


class UserBase(SQLModel):
    """Base class containing shared fields for User model."""
    username: str = Field(min_length=3, max_length=150, nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)


class User(UserBase, table=True):
    """
    User model for authentication data.
    Represents a user in the system with authentication-related fields.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against the hashed password.
        """
        from ..core.security import verify_password
        return verify_password(plain_password, hashed_password)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str  # Plain password, will be hashed before storing

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters due to bcrypt limitations')
        return v


class UserRead(UserBase):
    """Schema for reading user data (without sensitive information)."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserSignIn(SQLModel):
    """Schema for user sign in."""
    username: str
    password: str