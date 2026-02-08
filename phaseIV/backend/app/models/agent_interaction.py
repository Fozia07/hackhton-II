from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import JSON
import uuid

class AgentInteractionBase(SQLModel):
    message_id: str = Field(index=True)  # Which message triggered this interaction
    user_id: str = Field(index=True)  # Which user initiated the interaction
    tool_name: str = Field(max_length=100)  # Name of the MCP tool invoked
    tool_input: Dict[str, Any] = Field(default_factory=dict, sa_type=JSON)  # Input parameters passed to the tool
    tool_output: Dict[str, Any] = Field(default_factory=dict, sa_type=JSON)  # Output returned by the tool


class AgentInteraction(AgentInteractionBase, table=True):
    __tablename__ = "agent_interactions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    success: bool = Field(default=True)  # Whether the tool invocation succeeded
    error_message: Optional[str] = Field(default=None, max_length=1000)  # Error details if any

    # Relationships (if needed for joins in the future)
    # message: Optional["Message"] = Relationship(back_populates="agent_interactions")


class AgentInteractionCreate(AgentInteractionBase):
    pass


class AgentInteractionUpdate(SQLModel):
    success: Optional[bool] = None
    error_message: Optional[str] = None


class AgentInteractionRead(AgentInteractionBase):
    id: str
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None