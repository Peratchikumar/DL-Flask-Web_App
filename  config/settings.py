"""
Application configuration for Vehicle Damage Detection.

Single YOLO26 model configuration.
"""

from pathlib import Path
import os


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "Vehicle Damage Detection"
APP_VERSION = "1.0.0"

DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Single YOLO26 model
MODEL_PATH = BASE_DIR / "models" / "vehicle_damage_yolo26_best.pt"

# Image inference settings
IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "640"))

CONFIDENCE_THRESHOLD = float(
    os.getenv("CONFIDENCE_THRESHOLD", "0.25")
)

IOU_THRESHOLD = float(
    os.getenv("IOU_THRESHOLD", "0.45")
)


# ============================================================
# FILE STORAGE
# ============================================================

UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "outputs"


# Create required directories if they do not exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
}


ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "avi",
    "mov",
    "mkv",
    "webm",
}


# ============================================================
# UPLOAD LIMIT
# ============================================================

# 50 MB maximum upload size
MAX_CONTENT_LENGTH = 50 * 1024 * 1024


# ============================================================
# MODEL VALIDATION
# ============================================================

if not MODEL_PATH.exists():
    print(
        f"WARNING: YOLO26 model not found at: {MODEL_PATH}"
    )