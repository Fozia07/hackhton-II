from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(SQLModel):
    """Base class containing shared fields for Todo model."""
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    """
    Todo model for storing user tasks.
    Represents a todo item in the system with user relationship.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""
    pass


class TodoUpdate(SQLModel):
    """Schema for updating an existing todo."""
    title: Optional[str] = Field(default=None, min_length=0, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TodoRead(TodoBase):
    """Schema for reading todo data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime