import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "logs",
    "app.log"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database.db"
)

ENCODINGS_PATH = os.path.join(
    BASE_DIR,
    "encodings",
    "face_encodings.pkl"
)

UNKNOWN_FOLDER = os.path.join(
    BASE_DIR,
    "unknown_faces"
)

CAMERA_ID = 0

FRAME_RESIZE = 0.25

TOLERANCE = 0.45

ATTENDANCE_DELAY = 30

UNKNOWN_SAVE_INTERVAL = 10

os.makedirs(
    "logs",
    exist_ok=True
)

os.makedirs(
    UNKNOWN_FOLDER,
    exist_ok=True
)

os.makedirs(
    "encodings",
    exist_ok=True
)