from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
import uuid

class Base(SQLModel):
    """Base model with common fields"""
    id: Optional[str] = None

    def __init__(self, *args, **kwargs):
        if 'id' not in kwargs or kwargs['id'] is None:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(*args, **kwargs)