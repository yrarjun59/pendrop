# routers/journal.py
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

from database import HARDCODED_USER_ID, execute_query, execute_one, execute_write
from models import JournalEntry, JournalEntryCreate, JournalEntryUpdate

router = APIRouter(prefix="/api/journal", tags=["journal"])

def row_to_journal(row: dict) -> JournalEntry:
    return JournalEntry(
        id=row["id"],
        user_id=row["user_id"],
        title=row["title"],
        content=row["content"],
        mood=row["mood"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"])
    )

@router.get("", response_model=list[JournalEntry])
def list_entries(limit: int = 50, offset: int = 0):
    rows = execute_query(
        """
        SELECT * FROM journal_entries
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        (HARDCODED_USER_ID, limit, offset)
    )
    return [row_to_journal(row) for row in rows]

@router.post("", response_model=JournalEntry, status_code=201)
def create_entry(entry: JournalEntryCreate):
    entry_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    execute_write(
        """
        INSERT INTO journal_entries (id, user_id, title, content, mood, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (entry_id, HARDCODED_USER_ID, entry.title, entry.content, entry.mood, now, now)
    )
    
    row = execute_one("SELECT * FROM journal_entries WHERE id = ?", (entry_id,))
    return row_to_journal(row)

@router.get("/{entry_id}", response_model=JournalEntry)
def get_entry(entry_id: str):
    row = execute_one(
        "SELECT * FROM journal_entries WHERE id = ? AND user_id = ?",
        (entry_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Entry not found")
    return row_to_journal(row)

@router.put("/{entry_id}", response_model=JournalEntry)
def update_entry(entry_id: str, entry_update: JournalEntryUpdate):
    row = execute_one(
        "SELECT * FROM journal_entries WHERE id = ? AND user_id = ?",
        (entry_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    updates = []
    params = []
    if entry_update.title is not None:
        updates.append("title = ?")
        params.append(entry_update.title)
    if entry_update.content is not None:
        updates.append("content = ?")
        params.append(entry_update.content)
    if entry_update.mood is not None:
        updates.append("mood = ?")
        params.append(entry_update.mood)
    
    if updates:
        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(entry_id)
        execute_write(
            f"UPDATE journal_entries SET {', '.join(updates)} WHERE id = ?",
            tuple(params)
        )
    
    row = execute_one("SELECT * FROM journal_entries WHERE id = ?", (entry_id,))
    return row_to_journal(row)

@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: str):
    affected = execute_write(
        "DELETE FROM journal_entries WHERE id = ? AND user_id = ?",
        (entry_id, HARDCODED_USER_ID)
    )
    if affected == 0:
        raise HTTPException(status_code=404, detail="Entry not found")