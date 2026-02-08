from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # Scopes conversations to specific users
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True)

    # Relationship to messages in this conversation
    # messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ConversationRead(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool