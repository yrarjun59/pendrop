import sqlite3

conn = sqlite3.connect('backend/db/pendrop.db')

entries = [
    (1, 'Morning Reflection', 'Woke up early and spent 20 minutes meditating. Felt more clarity and focus throughout the day.'),
    (2, 'Learning AI Concepts', 'Studied gradient descent and backpropagation today. Still need to strengthen intuition on loss functions.'),
    (1, 'Business Idea Notes', 'Thinking about building an AI-powered writing assistant with minimal intervention. Focus on clarity first.'),
    (3, 'Daily Gratitude', 'Grateful for health, learning opportunities, and meaningful conversations today.'),
    (2, 'Project Progress Log', 'Implemented user authentication and basic CRUD for journal entries. Next step: add tagging system.')
]

for entry in entries:
    conn.execute('INSERT INTO journal_entries (user_id, title, content) VALUES (?, ?, ?)', entry)

conn.commit()
print(f"Inserted {len(entries)} journal entries!")

# Show all entries
cursor = conn.execute('SELECT id, user_id, title FROM journal_entries')
for row in cursor:
    print(row)

conn.close()