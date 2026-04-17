# models/chapter.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ChapterBase(BaseModel):
    book_id: str
    chapter_number: int
    title: str
    content: Optional[str] = None

class ChapterCreate(ChapterBase):
    pass

class ChapterUpdate(BaseModel):
    chapter_number: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None

class Chapter(ChapterBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True