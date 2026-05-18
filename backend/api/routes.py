from flask import Blueprint
from flask import render_template
from flask import Response
from flask import jsonify

import sqlite3
import cv2
import face_recognition
import pickle
import numpy as np

from datetime import datetime

api_bp = Blueprint("api", __name__)

DATABASE = "database.db"

camera = cv2.VideoCapture(0)

last_seen = {}

ATTENDANCE_DELAY = 30

print("[AI] Loading encodings...")

with open("encodings/face_encodings.pkl", "rb") as f:

    data = pickle.load(f)

print("[AI] Encodings loaded")


def mark_attendance(name):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
        SELECT * FROM attendance
        WHERE name=? AND date=?
    """, (name, today))

    result = cursor.fetchone()

    if result is None:

        cursor.execute("""
            INSERT INTO attendance
            (
                employee_id,
                name,
                date,
                first_in,
                last_out
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            name,
            today,
            current_time,
            current_time
        ))

        print(f"[IN] {name}")

    else:

        cursor.execute("""
            UPDATE attendance
            SET last_out=?
            WHERE name=? AND date=?
        """, (
            current_time,
            name,
            today
        ))

        print(f"[OUT] {name}")

    conn.commit()

    conn.close()


def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.25,
            fy=0.25
        )

        rgb_small = cv2.cvtColor(
            small_frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_small
        )

        face_encodings = face_recognition.face_encodings(
            rgb_small,
            face_locations
        )

        for face_encoding, face_location in zip(
            face_encodings,
            face_locations
        ):

            matches = face_recognition.compare_faces(
                data["encodings"],
                face_encoding,
                tolerance=0.45
            )

            face_distances = face_recognition.face_distance(
                data["encodings"],
                face_encoding
            )

            name = "Unknown"

            color = (0, 0, 255)

            confidence = 0

            if len(face_distances) > 0:

                best_match_index = np.argmin(
                    face_distances
                )

                confidence = round(
                    (1 - face_distances[best_match_index]) * 100,
                    2
                )

                if matches[best_match_index]:

                    name = data["names"][best_match_index]

                    color = (0, 255, 0)

                    if name not in last_seen:

                        mark_attendance(name)

                        last_seen[name] = datetime.now()

                    else:

                        seconds = (
                            datetime.now() -
                            last_seen[name]
                        ).seconds

                        if seconds > ATTENDANCE_DELAY:

                            mark_attendance(name)

                            last_seen[name] = datetime.now()

            top, right, bottom, left = face_location

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            label = f"{name} ({confidence}%)"

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )

            cv2.rectangle(
                frame,
                (left, bottom - 35),
                (right, bottom),
                color,
                cv2.FILLED
            )

            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

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

    return jsonify(data)


@api_bp.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )