# routers/snapshots.py
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

from database import HARDCODED_USER_ID, execute_query, execute_one, execute_write
from models import Snapshot, RestoreRequest

router = APIRouter(prefix="/api/chapters", tags=["snapshots"])

def row_to_snapshot(row: dict) -> Snapshot:
    return Snapshot(
        id=row["id"],
        chapter_id=row["chapter_id"],
        book_id=row["book_id"],
        content_json=row["content_json"],
        description=row["description"],
        created_at=datetime.fromisoformat(row["created_at"])
    )

@router.get("/{chapter_id}/snapshots", response_model=list[Snapshot])
def list_snapshots(chapter_id: str):
    row = execute_one(
        """
        SELECT c.id FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = ? AND b.user_id = ?
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    rows = execute_query(
        "SELECT * FROM snapshots WHERE chapter_id = ? ORDER BY created_at DESC",
        (chapter_id,)
    )
    return [row_to_snapshot(row) for row in rows]

@router.post("/{chapter_id}/snapshots", response_model=Snapshot, status_code=201)
def create_snapshot(chapter_id: str, description: str = None):
    chapter_row = execute_one(
        """
        SELECT c.id, c.book_id, c.content FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = ? AND b.user_id = ?
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if not chapter_row:
        raise HTTPException(status_code=404, detail="Chapter not found")
    if not chapter_row["content"]:
        raise HTTPException(status_code=400, detail="Chapter has no content to snapshot")
    
    snapshot_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    execute_write(
        """
        INSERT INTO snapshots (id, chapter_id, book_id, content_json, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (snapshot_id, chapter_id, chapter_row["book_id"], chapter_row["content"], description, now)
    )
    
    row = execute_one("SELECT * FROM snapshots WHERE id = ?", (snapshot_id,))
    return row_to_snapshot(row)

@router.post("/{chapter_id}/restore")
def restore_snapshot(chapter_id: str, request: RestoreRequest):
    chapter_row = execute_one(
        """
        SELECT c.id, c.book_id, c.content FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = ? AND b.user_id = ?
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if not chapter_row:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    snapshot_row = execute_one(
        "SELECT * FROM snapshots WHERE id = ? AND chapter_id = ?",
        (request.snapshot_id, chapter_id)
    )
    if not snapshot_row:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    
    # Create backup snapshot of current state
    if chapter_row["content"]:
        backup_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        execute_write(
            """
            INSERT INTO snapshots (id, chapter_id, book_id, content_json, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (backup_id, chapter_id, chapter_row["book_id"], chapter_row["content"],
             f"Auto-backup before restore from {request.snapshot_id}", now)
        )
    
    # Restore snapshot content
    execute_write(
        "UPDATE chapters SET content = ?, updated_at = ? WHERE id = ?",
        (snapshot_row["content_json"], datetime.utcnow().isoformat(), chapter_id)
    )
    
    return {"message": "Snapshot restored successfully"}