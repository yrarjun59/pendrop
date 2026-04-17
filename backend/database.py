import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

DB_PATH = "db/pendrop.db"
HARDCODED_USER_ID = "local-user"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return results as list of dicts."""
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

def execute_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Execute a SELECT query and return first result or None."""
    with get_db() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None

def execute_write(query: str, params: tuple = ()) -> int:
    """Execute INSERT/UPDATE/DELETE and return affected row count."""
    with get_db() as conn:
        cursor = conn.execute(query, params)
        return cursor.rowcount

def execute_insert(query: str, params: tuple = ()) -> int:
    """Execute INSERT and return the last inserted row ID."""
    with get_db() as conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid