# routers/chapters.py
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

from database import HARDCODED_USER_ID, execute_query, execute_one, execute_write
from models import Chapter, ChapterCreate, ChapterUpdate

router = APIRouter(prefix="/api", tags=["chapters"])

def row_to_chapter(row: dict) -> Chapter:
    return Chapter(
        id=row["id"],
        book_id=row["book_id"],
        chapter_number=row["chapter_number"],
        title=row["title"],
        content=row["content"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"])
    )

@router.get("/books/{book_id}/chapters", response_model=list[Chapter])
def list_chapters(book_id: str):
    book = execute_one(
        "SELECT id FROM books WHERE id = ? AND user_id = ?",
        (book_id, HARDCODED_USER_ID)
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    rows = execute_query(
        "SELECT * FROM chapters WHERE book_id = ? ORDER BY chapter_number",
        (book_id,)
    )
    return [row_to_chapter(row) for row in rows]

@router.post("/books/{book_id}/chapters", response_model=Chapter, status_code=201)
def create_chapter(book_id: str, chapter: ChapterCreate):
    if chapter.book_id != book_id:
        raise HTTPException(status_code=400, detail="book_id mismatch")
    
    book = execute_one(
        "SELECT id FROM books WHERE id = ? AND user_id = ?",
        (book_id, HARDCODED_USER_ID)
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    chapter_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    execute_write(
        """
        INSERT INTO chapters (id, book_id, chapter_number, title, content, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (chapter_id, book_id, chapter.chapter_number, chapter.title, chapter.content, now, now)
    )
    
    row = execute_one("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
    return row_to_chapter(row)

@router.get("/chapters/{chapter_id}", response_model=Chapter)
def get_chapter(chapter_id: str):
    row = execute_one(
        """
        SELECT c.* FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = ? AND b.user_id = ?
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return row_to_chapter(row)

@router.put("/chapters/{chapter_id}", response_model=Chapter)
def update_chapter(chapter_id: str, chapter_update: ChapterUpdate):
    row = execute_one(
        """
        SELECT c.* FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = ? AND b.user_id = ?
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    updates = []
    params = []
    if chapter_update.chapter_number is not None:
        updates.append("chapter_number = ?")
        params.append(chapter_update.chapter_number)
    if chapter_update.title is not None:
        updates.append("title = ?")
        params.append(chapter_update.title)
    if chapter_update.content is not None:
        updates.append("content = ?")
        params.append(chapter_update.content)
    
    if updates:
        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(chapter_id)
        execute_write(
            f"UPDATE chapters SET {', '.join(updates)} WHERE id = ?",
            tuple(params)
        )
    
    row = execute_one("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
    return row_to_chapter(row)

@router.delete("/chapters/{chapter_id}", status_code=204)
def delete_chapter(chapter_id: str):
    affected = execute_write(
        """
        DELETE FROM chapters
        WHERE id = ? AND book_id IN (SELECT id FROM books WHERE user_id = ?)
        """,
        (chapter_id, HARDCODED_USER_ID)
    )
    if affected == 0:
        raise HTTPException(status_code=404, detail="Chapter not found")