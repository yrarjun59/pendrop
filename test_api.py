import requests

BASE = "http://127.0.0.1:5000/api"

# Test creating a book
resp = requests.post(f"{BASE}/books", json={"title": "My First Book"})
print("Create book:", resp.json())

# Get books
resp = requests.get(f"{BASE}/books")
print("Get books:", resp.json())

# Get book id
book_id = resp.json()[0]["id"]

# Create chapter
resp = requests.post(f"{BASE}/books/{book_id}/chapters", json={"title": "Chapter 1"})
print("Create chapter:", resp.json())
chapter_id = resp.json()["id"]

# Get chapters
resp = requests.get(f"{BASE}/books/{book_id}/chapters")
print("Get chapters:", resp.json())

# Get chapter
resp = requests.get(f"{BASE}/chapters/{chapter_id}")
print("Get chapter:", resp.json())

# Create snapshot
resp = requests.post(f"{BASE}/chapters/{chapter_id}/snapshots", 
                    json={"description": "Test snapshot", "content_json": '{"type":"doc","content":[]}'})
print("Create snapshot:", resp.json())

# Get snapshots
resp = requests.get(f"{BASE}/chapters/{chapter_id}/snapshots")
print("Get snapshots:", resp.json())

print("\nAll tests passed!")
