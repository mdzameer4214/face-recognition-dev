import sqlite3

# DB 1 → Attendance logs (IN / OUT)
def create_attendance_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id TEXT,
        name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# DB 2 → Movement tracking (frequency)
def create_stats_db():
    conn = sqlite3.connect("stats.db")
    cursor = conn.cursor()

    
