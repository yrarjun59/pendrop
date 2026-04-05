from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib
import os
from datetime import datetime

from database import get_db, init_db
from models import (
    UserCreate, LoginRequest, JournalCreate, BookCreate, 
    ChapterCreate, SnapshotCreate, EssayCreate, FictionCreate, PoemCreate
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# AUTHENTICATION - Reserved for later implementation
# ============================================
# Placeholder for auth routes
# - POST /api/register
# - POST /api/login

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed


# ============================================
# JOURNAL ROUTES
# ============================================

@app.get("/api/journal/{user_id}")
def get_journals(user_id: int):
    conn = get_db()
    entries = conn.execute(
        "SELECT * FROM journal_entries WHERE user_id = ? ORDER BY created_at DESC", 
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in entries]

@app.post("/api/journal")
def create_journal(entry: JournalCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO journal_entries (user_id, title, content) VALUES (?, ?, ?)",
        (entry.user_id, entry.title, entry.content)
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return {"id": entry_id}

@app.put("/api/journal/{entry_id}")
def update_journal(entry_id: int, entry: JournalCreate):
    conn = get_db()
    conn.execute(
        "UPDATE journal_entries SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (entry.title, entry.content, entry_id)
    )
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/journal/{entry_id}")
def delete_journal(entry_id: int):
    conn = get_db()
    conn.execute("DELETE FROM journal_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# ============================================
# BOOKS ROUTES
# ============================================

@app.get("/api/books/{user_id}")
def get_books(user_id: int):
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
    return {"id": book_id}

@app.put("/api/books/{book_id}")
def update_book(book_id: int, book: BookCreate):
    conn = get_db()
    conn.execute(
        "UPDATE books SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (book.title, book_id)
    )
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
# CHAPTERS & SUB-CHAPTERS ROUTES
# ============================================

@app.get("/api/chapters/{book_id}")
def get_chapters(book_id: int):
    conn = get_db()
    chapters = conn.execute(
        "SELECT * FROM chapters WHERE book_id = ? ORDER BY order_index", 
        (book_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in chapters]

@app.post("/api/chapters")
def create_chapter(chapter: ChapterCreate):
    conn = get_db()
    
    # Get next order index
    if chapter.parent_chapter_id:
        max_order = conn.execute(
            "SELECT MAX(order_index) as max_order FROM chapters WHERE parent_chapter_id = ?",
            (chapter.parent_chapter_id,)
        ).fetchone()["max_order"] or 0
    else:
        max_order = conn.execute(
            "SELECT MAX(order_index) as max_order FROM chapters WHERE book_id = ? AND parent_chapter_id IS NULL",
            (chapter.book_id,)
        ).fetchone()["max_order"] or 0
    
    next_order = max_order + 1
    
    cursor = conn.execute(
        "INSERT INTO chapters (book_id, title, content, order_index, parent_chapter_id) VALUES (?, ?, ?, ?, ?)",
        (chapter.book_id, chapter.title, chapter.content, next_order, chapter.parent_chapter_id)
    )
    conn.commit()
    chapter_id = cursor.lastrowid
    conn.close()
    return {"id": chapter_id}

@app.put("/api/chapters/{chapter_id}")
def update_chapter(chapter_id: int, chapter: ChapterCreate):
    conn = get_db()
    conn.execute(
        "UPDATE chapters SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (chapter.title, chapter.content, chapter_id)
    )
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/chapters/{chapter_id}")
def delete_chapter(chapter_id: int):
    conn = get_db()
    # Delete sub-chapters first
    conn.execute("DELETE FROM chapters WHERE parent_chapter_id = ?", (chapter_id,))
    conn.execute("DELETE FROM snapshots WHERE chapter_id = ?", (chapter_id,))
    conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# ============================================
# SNAPSHOTS ROUTES (Books only)
# ============================================

@app.post("/api/snapshots")
def create_snapshot(snap: SnapshotCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO snapshots (chapter_id, content, note) VALUES (?, ?, ?)",
        (snap.chapter_id, snap.content, snap.note)
    )
    conn.commit()
    snapshot_id = cursor.lastrowid
    conn.close()
    return {"id": snapshot_id}

@app.get("/api/snapshots/{chapter_id}")
def get_snapshots(chapter_id: int):
    conn = get_db()
    snaps = conn.execute(
        "SELECT * FROM snapshots WHERE chapter_id = ? ORDER BY created_at DESC", 
        (chapter_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in snaps]


# ============================================
# ESSAYS ROUTES
# ============================================

@app.get("/api/essays/{user_id}")
def get_essays(user_id: int):
    conn = get_db()
    essays = conn.execute(
        "SELECT * FROM essays WHERE user_id = ? ORDER BY updated_at DESC", 
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in essays]

@app.post("/api/essays")
def create_essay(essay: EssayCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO essays (user_id, title, content) VALUES (?, ?, ?)",
        (essay.user_id, essay.title, essay.content)
    )
    conn.commit()
    essay_id = cursor.lastrowid
    conn.close()
    return {"id": essay_id}

@app.put("/api/essays/{essay_id}")
def update_essay(essay_id: int, essay: EssayCreate):
    conn = get_db()
    conn.execute(
        "UPDATE essays SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (essay.title, essay.content, essay_id)
    )
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/essays/{essay_id}")
def delete_essay(essay_id: int):
    conn = get_db()
    conn.execute("DELETE FROM essays WHERE id = ?", (essay_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# ============================================
# FICTION ROUTES
# ============================================

@app.get("/api/fictions/{user_id}")
def get_fictions(user_id: int):
    conn = get_db()
    fictions = conn.execute(
        "SELECT * FROM fictions WHERE user_id = ? ORDER BY updated_at DESC", 
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in fictions]

@app.post("/api/fictions")
def create_fiction(fiction: FictionCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO fictions (user_id, title, content) VALUES (?, ?, ?)",
        (fiction.user_id, fiction.title, fiction.content)
    )
    conn.commit()
    fiction_id = cursor.lastrowid
    conn.close()
    return {"id": fiction_id}

@app.put("/api/fictions/{fiction_id}")
def update_fiction(fiction_id: int, fiction: FictionCreate):
    conn = get_db()
    conn.execute(
        "UPDATE fictions SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (fiction.title, fiction.content, fiction_id)
    )
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/fictions/{fiction_id}")
def delete_fiction(fiction_id: int):
    conn = get_db()
    conn.execute("DELETE FROM fictions WHERE id = ?", (fiction_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# ============================================
# POEMS ROUTES
# ============================================

@app.get("/api/poems/{user_id}")
def get_poems(user_id: int):
    conn = get_db()
    poems = conn.execute(
        "SELECT * FROM poems WHERE user_id = ? ORDER BY updated_at DESC", 
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in poems]

@app.post("/api/poems")
def create_poem(poem: PoemCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO poems (user_id, title, content) VALUES (?, ?, ?)",
        (poem.user_id, poem.title, poem.content)
    )
    conn.commit()
    poem_id = cursor.lastrowid
    conn.close()
    return {"id": poem_id}

@app.put("/api/poems/{poem_id}")
def update_poem(poem_id: int, poem: PoemCreate):
    conn = get_db()
    conn.execute(
        "UPDATE poems SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (poem.title, poem.content, poem_id)
    )
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/poems/{poem_id}")
def delete_poem(poem_id: int):
    conn = get_db()
    conn.execute("DELETE FROM poems WHERE id = ?", (poem_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=5000)