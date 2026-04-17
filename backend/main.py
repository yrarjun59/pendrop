# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import routers
import uvicorn

app = FastAPI(
    title="Pendrop API",
    version="1.0.0",
    description="A local-first writing application for books and journals"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
for router in routers:
    app.include_router(router)

@app.get("/")
def root():
    return {
        "name": "Pendrop API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "books": "/api/books",
            "chapters": "/api/books/{book_id}/chapters",
            "snapshots": "/api/chapters/{chapter_id}/snapshots",
            "journal": "/api/journal"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=3333,
        reload=True,
        reload_dirs=["."],
        log_level="info"
    )