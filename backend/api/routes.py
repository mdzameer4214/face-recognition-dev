from flask import Blueprint
from flask import render_template

import sqlite3
from datetime import datetime

api_bp = Blueprint("api", __name__)

DATABASE = "database.db"


@api_bp.route("/")
def dashboard():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """)

    attendance = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(DISTINCT name)
        FROM attendance
    """)

    total = cursor.fetchone()[0]

    today_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE date=?
    """, (today_date,))

    today = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        attendance=attendance,
        total=total,
        today=today
    )


@api_bp.route("/health")
def health():

    return {
        "status": "healthy"
    }


@api_bp.route("/attendance")
def attendance_api():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({
            "id": row["id"],
            "employee_id": row["employee_id"],
            "name": row["name"],
            "date": row["date"],
            "first_in": row["first_in"],
            "last_out": row["last_out"]
        })

    return {
        "attendance": data
    }