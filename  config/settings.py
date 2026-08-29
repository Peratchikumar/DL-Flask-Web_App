"""
Application configuration settings.

Vehicle Damage Detection
YOLO26 + Flask
"""

import os
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Using ONLY the PyTorch YOLO model (.pt)
MODEL_PATH = BASE_DIR / "models" / "vehicle_damage_yolo26_best.pt"


# ============================================================
# YOLO DETECTION SETTINGS
# ============================================================

CONFIDENCE_THRESHOLD = float(
    os.getenv("CONFIDENCE_THRESHOLD", "0.25")
)

IOU_THRESHOLD = float(
    os.getenv("IOU_THRESHOLD", "0.45")
)


# ============================================================
# FILE / DIRECTORY CONFIGURATION
# ============================================================

UPLOAD_FOLDER = BASE_DIR / "uploads"

OUTPUT_FOLDER = BASE_DIR / "outputs"


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv",
    "webm"
}


# ============================================================
# FLASK CONFIGURATION
# ============================================================

MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "vehicle-damage-detection-secret-key"
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "Vehicle Damage Detection"

APP_VERSION = "1.0.0"

DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# VALIDATE MODEL
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found: {MODEL_PATH}"
    )