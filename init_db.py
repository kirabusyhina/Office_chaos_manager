import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT,
    priority TEXT
)
""")

conn.commit()
conn.close()

print("Database created!")