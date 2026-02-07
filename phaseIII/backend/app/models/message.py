from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class MessageBase(SQLModel):
    conversation_id: str = Field(index=True)
    user_id: str = Field(index=True)  # Who sent the message
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(min_length=1)
    sequence_number: Optional[int] = Field(default=None)  # Order of message in conversation


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships (if needed for joins in the future)
    # conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    role: Optional[str] = None


class MessageRead(MessageBase):
    id: str
    timestamp: datetime