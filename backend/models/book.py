# models/book.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

from models.chapter import Chapter

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Book(BookBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    # chapters: here 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookWithChapters(Book):
    chapters: List[Chapter] = []