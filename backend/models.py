from pydantic import BaseModel
from typing import Optional

# Request Models

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class JournalCreate(BaseModel):
    user_id: int
    title: str
    content: str = ""

class BookCreate(BaseModel):
    user_id: int
    title: str

class ChapterCreate(BaseModel):
    book_id: int
    title: str
    content: str = ""
    parent_chapter_id: Optional[int] = None

class SnapshotCreate(BaseModel):
    chapter_id: int
    content: str
    note: str = ""

class EssayCreate(BaseModel):
    user_id: int
    title: str
    content: str = ""

class FictionCreate(BaseModel):
    user_id: int
    title: str
    content: str = ""

class PoemCreate(BaseModel):
    user_id: int
    title: str
    content: str = ""

# Response Models

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

class JournalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class BookResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class ChapterResponse(BaseModel):
    id: int
    book_id: int
    title: str
    content: str
    order_index: int
    parent_chapter_id: Optional[int]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class SnapshotResponse(BaseModel):
    id: int
    chapter_id: int
    content: str
    note: str
    created_at: str
    
    class Config:
        from_attributes = True

class EssayResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class FictionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class PoemResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True