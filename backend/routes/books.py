from fastapi import APIRouter, HTTPException, Query
import uuid
from datetime import datetime
from typing import List

from database import HARDCODED_USER_ID, execute_query, execute_one, execute_write
from models import Book, BookCreate, BookUpdate, BookWithChapters, Chapter

router = APIRouter(prefix="/api", tags=["books"])

def row_to_book(row: dict) -> Book:
    return Book(
        id=row["id"],
        user_id=row["user_id"],
        title=row["title"],
        description=row["description"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"])
    )

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

def get_chapters_for_book(book_id: str) -> List[Chapter]:
    """Helper function to fetch all chapters for a given book."""
    chapter_rows = execute_query(
        "SELECT * FROM chapters WHERE book_id = ? ORDER BY chapter_number",
        (book_id,)
    )
    return [row_to_chapter(row) for row in chapter_rows]

# ---------- List Books (with chapters) ----------
@router.get("/books", response_model=List[BookWithChapters])
def list_books(include_chapters: bool = Query(True, description="Include chapters in each book")):
    rows = execute_query(
        "SELECT * FROM books WHERE user_id = ? ORDER BY updated_at DESC",
        (HARDCODED_USER_ID,)
    )
    
    books_with_chapters = []
    for row in rows:
        book = row_to_book(row)
        
        if include_chapters:
            chapters = get_chapters_for_book(book.id)
            books_with_chapters.append(
                BookWithChapters(
                    id=book.id,
                    user_id=book.user_id,
                    title=book.title,
                    description=book.description,
                    chapters=chapters,
                    created_at=book.created_at,
                    updated_at=book.updated_at,
                )
            )
        else:
            # Still wrap in BookWithChapters but with empty chapters list
            books_with_chapters.append(
                BookWithChapters(
                    id=book.id,
                    user_id=book.user_id,
                    title=book.title,
                    chapters=[],
                    description=book.description,
                    created_at=book.created_at,
                    updated_at=book.updated_at
                )
            )
    
    return books_with_chapters

# ---------- Create Book ----------
@router.post("/create-book/", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    book_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    execute_write(
        """
        INSERT INTO books (id, user_id, title, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (book_id, HARDCODED_USER_ID, book.title, book.description, now, now)
    )
    
    row = execute_one("SELECT * FROM books WHERE id = ?", (book_id,))
    return row_to_book(row)

# ---------- Get Single Book (with chapters) ----------
@router.get("/book/{book_id}", response_model=BookWithChapters)
def get_book(
    book_id: str,
    include_chapters: bool = Query(True, description="Include chapters in the response")
):
    book_row = execute_one(
        "SELECT * FROM books WHERE id = ? AND user_id = ?",
        (book_id, HARDCODED_USER_ID)
    )
    if not book_row:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = row_to_book(book_row)
    chapters = get_chapters_for_book(book_id) if include_chapters else []
    
    return BookWithChapters(
        id=book.id,
        user_id=book.user_id,
        title=book.title,
        description=book.description,
        chapters=chapters,
        created_at=book.created_at,
        updated_at=book.updated_at
        
    )

# ---------- Update Book ----------
@router.put("/book/update/{book_id}", response_model=Book)
def update_book(book_id: str, book_update: BookUpdate):
    row = execute_one(
        "SELECT * FROM books WHERE id = ? AND user_id = ?",
        (book_id, HARDCODED_USER_ID)
    )
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updates = []
    params = []
    if book_update.title is not None:
        updates.append("title = ?")
        params.append(book_update.title)
    if book_update.description is not None:
        updates.append("description = ?")
        params.append(book_update.description)
    
    if updates:
        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(book_id)
        execute_write(
            f"UPDATE books SET {', '.join(updates)} WHERE id = ?",
            tuple(params)
        )
    
    row = execute_one("SELECT * FROM books WHERE id = ?", (book_id,))
    return row_to_book(row)

# ---------- Delete Book ----------
@router.delete("/book/delete/{book_id}", status_code=204)
def delete_book(book_id: str):
    affected = execute_write(
        "DELETE FROM books WHERE id = ? AND user_id = ?",
        (book_id, HARDCODED_USER_ID)
    )
    if affected == 0:
        raise HTTPException(status_code=404, detail="Book not found")