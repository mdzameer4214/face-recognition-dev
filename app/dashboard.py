from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE_PATH = "database/database.db"


@app.route("/")
def index():

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """)

    attendance_data = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT name) as total
        FROM attendance
        WHERE DATE(date) = DATE('now')
    """)

    total_people = cursor.fetchone()["total"]

    conn.close()

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return render_template(
        "index.html",
        attendance=attendance_data,
        total_people=total_people,
        current_time=current_time
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
