"""
Vehicle Damage Detection
Flask Application
"""

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template
from werkzeug.exceptions import RequestEntityTooLarge


# ============================================================
# PROJECT ROOT / PYTHON PATH
# ============================================================

# Get the folder where app.py is located
BASE_DIR = Path(__file__).resolve().parent

# Make sure Python can find config/, routes/, services/, utils/, etc.
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

from config.settings import (
    APP_NAME,
    APP_VERSION,
    DEBUG,
    MAX_CONTENT_LENGTH,
)


# ============================================================
# ROUTES
# ============================================================

from routes.prediction import prediction_bp


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# ============================================================
# REGISTER BLUEPRINT
# ============================================================

app.register_blueprint(
    prediction_bp,
    url_prefix="/api",
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET"])
def home():
    """
    Render the main frontend.
    """

    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health-check endpoint for deployment platforms.
    """

    return jsonify({
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
    }), 200


# ============================================================
# APPLICATION INFORMATION
# ============================================================

@app.route("/api/info", methods=["GET"])
def application_info():
    """
    Return basic application information.
    """

    return jsonify({
        "success": True,
        "application": APP_NAME,
        "version": APP_VERSION,
        "model": "YOLO26",
        "model_format": "PyTorch (.pt)",
        "model_count": 1,
    }), 200


# ============================================================
# FILE SIZE ERROR
# ============================================================

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    """
    Handle files exceeding the configured upload limit.
    """

    return jsonify({
        "success": False,
        "error": "File too large.",
        "message": (
            "The uploaded file exceeds "
            "the maximum allowed size."
        ),
    }), 413


# ============================================================
# GENERAL ERROR HANDLER
# ============================================================

@app.errorhandler(Exception)
def handle_general_error(error):
    """
    Handle unexpected application errors.
    """

    app.logger.exception(
        "Unexpected application error: %s",
        error,
    )

    return jsonify({
        "success": False,
        "error": "Internal server error.",
        "message": (
            "An unexpected error occurred "
            "while processing the request."
        ),
    }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    # Render provides the PORT environment variable.
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=DEBUG,
    )