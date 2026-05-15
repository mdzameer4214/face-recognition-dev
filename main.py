import cv2
import face_recognition
import pickle
import numpy as np
import sqlite3
import os
import logging
from datetime import datetime

import config

# ======================
# LOGGING
# ======================
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

print("[INFO] Loading encodings...")

# ======================
# LOAD ENCODINGS
# ======================
with open(config.ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

print("[INFO] Encodings loaded")

# ======================
# DATABASE
# ======================
conn = sqlite3.connect(config.DATABASE_PATH, check_same_thread=False)
cursor = conn.cursor()

# ======================
# TABLES
# ======================
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS movement_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    event TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS unknown_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

# ======================
# CAMERA
# ======================
video = cv2.VideoCapture(config.CAMERA_ID)

print("[INFO] Camera started")

# ======================
# TRACKERS
# ======================
last_seen = {}
last_unknown_save = {}

# ======================
# ATTENDANCE FUNCTION
# ======================
def mark_attendance(name):

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    cursor.execute(
        "SELECT * FROM attendance WHERE name=? AND date=?",
        (name, date)
    )

    result = cursor.fetchone()

    # FIRST TIME ENTRY
    if result is None:

        cursor.execute("""
            INSERT INTO attendance
            (employee_id, name, date, first_in, last_out)
            VALUES (?, ?, ?, ?, ?)
        """, (name, name, date, current_time, current_time))

        # IN EVENT
        cursor.execute("""
            INSERT INTO movement_log
            (name, date, time, event)
            VALUES (?, ?, ?, ?)
        """, (name, date, current_time, "IN"))

        conn.commit()

        print(f"[IN] {name}")

    # EXISTING USER (OUT / UPDATE)
    else:

        cursor.execute("""
            UPDATE attendance
            SET last_out=?
            WHERE name=? AND date=?
        """, (current_time, name, date))

        # OUT EVENT
        cursor.execute("""
            INSERT INTO movement_log
            (name, date, time, event)
            VALUES (?, ?, ?, ?)
        """, (name, date, current_time, "OUT"))

        conn.commit()

        print(f"[OUT] {name}")

# ======================
# MAIN LOOP
# ======================
print("[INFO] Running system...")

while True:

    ret, frame = video.read()
    if not ret:
        break

    small = cv2.resize(frame, (0, 0), fx=config.FRAME_RESIZE, fy=config.FRAME_RESIZE)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):

        matches = face_recognition.compare_faces(
            data["encodings"],
            encoding,
            tolerance=config.TOLERANCE
        )

        distances = face_recognition.face_distance(
            data["encodings"],
            encoding
        )

        name = "Unknown"
        confidence = 0
        color = (0, 0, 255)

        if len(distances) > 0:

            best_match = np.argmin(distances)
            confidence = round((1 - distances[best_match]) * 100, 2)

            if matches[best_match]:

                name = data["names"][best_match]
                color = (0, 255, 0)

                if name not in last_seen:

                    mark_attendance(name)
                    last_seen[name] = datetime.now()

                else:

                    seconds = (datetime.now() - last_seen[name]).seconds

                    if seconds > config.ATTENDANCE_DELAY:

                        mark_attendance(name)
                        last_seen[name] = datetime.now()

        # UNKNOWN PERSON
        if name == "Unknown":

            now = datetime.now()

            if "unknown" not in last_unknown_save or \
               (now - last_unknown_save["unknown"]).seconds > config.UNKNOWN_SAVE_INTERVAL:

                filename = f"{datetime.now().timestamp()}.jpg"
                filepath = os.path.join(config.UNKNOWN_FOLDER, filename)

                cv2.imwrite(filepath, frame)

                cursor.execute("""
                    INSERT INTO unknown_log
                    (image_path, date, time)
                    VALUES (?, ?, ?)
                """, (
                    filepath,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S")
                ))

                conn.commit()

                last_unknown_save["unknown"] = now

                print("[UNKNOWN DETECTED]")

        # DRAW BOX
        top, right, bottom, left = box
        scale = int(1 / config.FRAME_RESIZE)

        top *= scale
        right *= scale
        bottom *= scale
        left *= scale

        label = f"{name} ({confidence}%)"

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

        cv2.putText(frame, label, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Face Recognition System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
conn.close()