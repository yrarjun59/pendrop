# models/snapshot.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class SnapshotBase(BaseModel):
    chapter_id: str
    book_id: str
    content_json: str
    description: Optional[str] = None

class SnapshotCreate(SnapshotBase):
    pass

class Snapshot(SnapshotBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime

    class Config:
        from_attributes = True

class RestoreRequest(BaseModel):
    snapshot_id: str