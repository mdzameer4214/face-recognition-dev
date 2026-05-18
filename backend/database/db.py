import sqlite3

from backend.core.config import DATABASE_PATH


def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn