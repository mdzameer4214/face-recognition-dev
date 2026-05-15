import sqlite3
import pandas as pd
import os

os.makedirs("exports", exist_ok=True)

conn = sqlite3.connect("database/database.db")

query = """
SELECT
    employee_id,
    name,
    date,
    first_in,
    last_out
FROM attendance
"""

df = pd.read_sql_query(query, conn)

export_path = "exports/attendance.xlsx"

df.to_excel(export_path, index=False)

conn.close()

print(f"Attendance exported successfully: {export_path}")
