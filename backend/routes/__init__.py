# routers/__init__.py
from routes.books import router as books_router
from routes.chapters import router as chapters_router
from routes.snapshots import router as snapshots_router
from routes.journals import router as journal_router

routers = [books_router, chapters_router, snapshots_router, journal_router]