# models/journal.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class JournalEntryBase(BaseModel):
    title: Optional[str] = None
    content: str
    mood: Optional[str] = None

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None

class JournalEntry(JournalEntryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True