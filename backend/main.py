"""
PenDrop Backend - FastAPI with SQLite
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db, init_db

app = FastAPI()

# Serve frontend static files
@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html"))

@app.get("/css/{filename}")
async def serve_css(filename: str):
    return FileResponse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "css", filename))

@app.get("/js/{filename}")
async def serve_js(filename: str):
    return FileResponse(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "js", filename))

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class BookCreate(BaseModel):
    title: str
    user_id: int = 1

class BookUpdate(BaseModel):
    title: Optional[str] = None

class ChapterCreate(BaseModel):
    title: str
    parent_id: Optional[int] = None
    content: Optional[str] = None

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    parent_id: Optional[int] = None
    position: Optional[int] = None

class SnapshotCreate(BaseModel):
    description: Optional[str] = None
    content_json: Optional[str] = None

class RestoreRequest(BaseModel):
    snapshot_id: int

class JournalCreate(BaseModel):
    title: str = "Untitled"
    content: str = ""
    user_id: int = 1

class JournalUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# ============================================
# BOOKS ROUTES
# ============================================

@app.get("/api/books")
def get_books(user_id: int = 1):
    conn = get_db()
    books = conn.execute(
        "SELECT * FROM books WHERE user_id = ? ORDER BY updated_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in books]

@app.post("/api/books")
def create_book(book: BookCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO books (user_id, title) VALUES (?, ?)",
        (book.user_id, book.title)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return {"id": book_id, "title": book.title, "user_id": book.user_id}

@app.get("/api/books/{book_id}")
def get_book(book_id: int):
    conn = get_db()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(book)

@app.put("/api/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    conn = get_db()
    updates = []
    values = []
    
    if book.title is not None:
        updates.append("title = ?")
        values.append(book.title)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(book_id)
        conn.execute(f"UPDATE books SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()
    
    conn.close()
    return {"status": "updated"}

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    conn = get_db()
    conn.execute("DELETE FROM chapters WHERE book_id = ?", (book_id,))
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

# ============================================
# CHAPTERS ROUTES
# ============================================

@app.get("/api/books/{book_id}/chapters")
def get_chapters(book_id: int):
    conn = get_db()
    chapters = conn.execute(
        "SELECT * FROM chapters WHERE book_id = ? ORDER BY position, id",
        (book_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in chapters]

@app.post("/api/books/{book_id}/chapters")
def create_chapter(book_id: int, chapter: ChapterCreate):
    conn = get_db()
    
    # Get next position
    max_pos = conn.execute(
        "SELECT MAX(position) as max_pos FROM chapters WHERE book_id = ? AND parent_id IS ?",
        (book_id, chapter.parent_id)
    ).fetchone()["max_pos"] or 0
    
    cursor = conn.execute(
        "INSERT INTO chapters (book_id, parent_id, title, content, position) VALUES (?, ?, ?, ?, ?)",
        (book_id, chapter.parent_id, chapter.title, chapter.content or "", max_pos + 1)
    )
    conn.commit()
    chapter_id = cursor.lastrowid
    conn.close()
    
    return {"id": chapter_id, "book_id": book_id, "title": chapter.title, "parent_id": chapter.parent_id}

@app.get("/api/chapters/{chapter_id}")
def get_chapter(chapter_id: int):
    conn = get_db()
    chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    conn.close()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return dict(chapter)

@app.put("/api/chapters/{chapter_id}")
def update_chapter(chapter_id: int, chapter: ChapterUpdate):
    conn = get_db()
    updates = []
    values = []
    
    if chapter.title is not None:
        updates.append("title = ?")
        values.append(chapter.title)
    
    if chapter.content is not None:
        updates.append("content = ?")
        values.append(chapter.content)
    
    if chapter.parent_id is not None:
        updates.append("parent_id = ?")
        values.append(chapter.parent_id)
    
    if chapter.position is not None:
        updates.append("position = ?")
        values.append(chapter.position)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(chapter_id)
        conn.execute(f"UPDATE chapters SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()
        
        # Update book's updated_at
        chapter_data = conn.execute("SELECT book_id FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
        if chapter_data:
            conn.execute("UPDATE books SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (chapter_data["book_id"],))
            conn.commit()
    
    conn.close()
    return {"status": "updated"}

@app.delete("/api/chapters/{chapter_id}")
def delete_chapter(chapter_id: int):
    conn = get_db()
    # Delete child chapters first
    conn.execute("DELETE FROM chapters WHERE parent_id = ?", (chapter_id,))
    # Delete snapshots
    conn.execute("DELETE FROM snapshots WHERE chapter_id = ?", (chapter_id,))
    # Delete chapter
    conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

# ============================================
# SNAPSHOTS ROUTES
# ============================================

@app.get("/api/chapters/{chapter_id}/snapshots")
def get_snapshots(chapter_id: int):
    conn = get_db()
    snapshots = conn.execute(
        "SELECT * FROM snapshots WHERE chapter_id = ? ORDER BY created_at DESC",
        (chapter_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in snapshots]

@app.post("/api/chapters/{chapter_id}/snapshots")
def create_snapshot(chapter_id: int, snap: SnapshotCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO snapshots (chapter_id, content_json, description) VALUES (?, ?, ?)",
        (chapter_id, snap.content_json or "", snap.description or "Manual save")
    )
    conn.commit()
    snapshot_id = cursor.lastrowid
    conn.close()
    return {"id": snapshot_id}

@app.post("/api/chapters/{chapter_id}/restore")
def restore_snapshot(chapter_id: int, req: RestoreRequest):
    conn = get_db()
    
    # Get snapshot content
    snapshot = conn.execute("SELECT content_json FROM snapshots WHERE id = ? AND chapter_id = ?",
                           (req.snapshot_id, chapter_id)).fetchone()
    
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    
    # Update chapter with snapshot content
    conn.execute("UPDATE chapters SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (snapshot["content_json"], chapter_id))
    conn.commit()
    conn.close()
    
    return {"status": "restored"}

# ============================================
# JOURNAL ROUTES
# ============================================

@app.get("/api/journal")
def get_journal(user_id: int = 1):
    conn = get_db()
    entries = conn.execute(
        "SELECT * FROM journal_entries WHERE user_id = ? ORDER BY updated_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in entries]

@app.post("/api/journal")
def create_journal_entry(entry: JournalCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO journal_entries (user_id, title, content) VALUES (?, ?, ?)",
        (entry.user_id, entry.title, entry.content)
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return {"id": entry_id, "title": entry.title}

@app.get("/api/journal/{entry_id}")
def get_journal_entry(entry_id: int):
    conn = get_db()
    entry = conn.execute("SELECT * FROM journal_entries WHERE id = ?", (entry_id,)).fetchone()
    conn.close()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return dict(entry)

@app.put("/api/journal/{entry_id}")
def update_journal_entry(entry_id: int, entry: JournalUpdate):
    conn = get_db()
    updates = []
    values = []
    
    if entry.title is not None:
        updates.append("title = ?")
        values.append(entry.title)
    
    if entry.content is not None:
        updates.append("content = ?")
        values.append(entry.content)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(entry_id)
        conn.execute(f"UPDATE journal_entries SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()
    
    conn.close()
    return {"status": "updated"}

@app.delete("/api/journal/{entry_id}")
def delete_journal_entry(entry_id: int):
    conn = get_db()
    conn.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)
