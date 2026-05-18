from pathlib import Path
import os

# =========================
# BASE PROJECT DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =========================
# DATABASE
# =========================

DATABASE_PATH = BASE_DIR / "database.db"

# =========================
# ENCODINGS
# =========================

ENCODINGS_DIR = BASE_DIR / "encodings"

ENCODINGS_PATH = ENCODINGS_DIR / "face_encodings.pkl"

# =========================
# UNKNOWN FACES
# =========================

UNKNOWN_FACES_DIR = BASE_DIR / "unknown_faces"

# =========================
# LOGS
# =========================

LOGS_DIR = BASE_DIR / "logs"

LOG_FILE = LOGS_DIR / "app.log"

# =========================
# DATASET
# =========================

DATASET_DIR = BASE_DIR / "dataset"

# =========================
# CAMERA SETTINGS
# =========================

CAMERA_ID = 0

FRAME_RESIZE = 0.25

TOLERANCE = 0.45

# =========================
# SYSTEM SETTINGS
# =========================

ATTENDANCE_DELAY = 30

UNKNOWN_SAVE_INTERVAL = 10

# =========================
# AUTO CREATE DIRECTORIES
# =========================

ENCODINGS_DIR.mkdir(exist_ok=True)

UNKNOWN_FACES_DIR.mkdir(exist_ok=True)

LOGS_DIR.mkdir(exist_ok=True)