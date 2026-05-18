from flask import Blueprint
from flask import render_template
from flask import Response

import sqlite3
import cv2

from datetime import datetime

api_bp = Blueprint("api", __name__)

DATABASE = "database.db"

camera = cv2.VideoCapture(0)


def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        else:

            ret, buffer = cv2.imencode(".jpg", frame)

            frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame +
                b"\r\n"
            )


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


@api_bp.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )