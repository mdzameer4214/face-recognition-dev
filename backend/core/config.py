import os
from pathlib import Path

# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# DATABASE
# =========================

DATABASE_PATH = BASE_DIR / "database" / "database.db"

# =========================
# LOGS
# =========================

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "app.log"

# =========================
# ENCODINGS
# =========================

ENCODINGS_DIR = BASE_DIR / "encodings"
ENCODINGS_DIR.mkdir(exist_ok=True)

ENCODINGS_PATH = ENCODINGS_DIR / "face_encodings.pkl"

# =========================
# UNKNOWN FACES
# =========================

UNKNOWN_DIR = BASE_DIR / "unknown_faces"
UNKNOWN_DIR.mkdir(exist_ok=True)

# =========================
# DATASET
# =========================

DATASET_DIR = BASE_DIR.parent / "dataset"

# =========================
# CAMERA SETTINGS
# =========================

CAMERA_ID = 0

FRAME_RESIZE = 0.25

TOLERANCE = 0.45

# =========================
# ATTENDANCE SETTINGS
# =========================

ATTENDANCE_DELAY = 30

UNKNOWN_SAVE_INTERVAL = 10

# =========================
# SECURITY
# =========================

ENABLE_UNKNOWN_CAPTURE = True

ENABLE_LOGGING = True

# =========================
# DASHBOARD
# =========================

DASHBOARD_HOST = "0.0.0.0"

DASHBOARD_PORT = 5001

DEBUG_MODE = True

# =========================
# AI ENGINE
# =========================

FACE_DETECTION_MODEL = "hog"

# hog = CPU
# cnn = GPU (future)