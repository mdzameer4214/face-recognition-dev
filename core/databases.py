import sqlite3

# ================= ATTENDANCE DATABASE =================
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id TEXT,
    name TEXT,
    date TEXT,
    first_in TEXT,
    last_out TEXT
)
""")

conn.commit()
conn.close()


# ================= MOVEMENT DATABASE =================
conn = sqlite3.connect("movement.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movement (
    id TEXT,
    name TEXT,
    status TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS movement_stats (
    id TEXT PRIMARY KEY,
    name TEXT,
    count INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Databases created successfully")
