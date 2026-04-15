"""
PenDrop - App Launcher
Opens the app in your default browser
"""

import webbrowser
import threading
import time
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_backend():
    """Start FastAPI backend server"""
    import uvicorn
    from backend.main import app
    
    print("Starting PenDrop backend...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def main():
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    time.sleep(2)
    
    # Open in browser
    print("Opening PenDrop in browser...")
    webbrowser.open('http://127.0.0.1:8000/')
    
    print("\nPenDrop is running!")
    print("Press Ctrl+C to stop the server")

if __name__ == "__main__":
    main()
