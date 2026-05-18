from backend.database.db import get_connection


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================
    # ATTENDANCE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        name TEXT,
        date TEXT,
        first_in TEXT,
        last_out TEXT
    )
    """)

    # =========================
    # MOVEMENT LOG
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movement_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT,
        event TEXT
    )
    """)

    # =========================
    # UNKNOWN LOG
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unknown_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()

    conn.close()

    print("[DATABASE] Tables initialized")