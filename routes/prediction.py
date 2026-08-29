"""
Prediction API Routes.

Vehicle Damage Detection
YOLO26 + Flask
"""

from pathlib import Path
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from config.settings import (
    UPLOAD_FOLDER,
    ALLOWED_IMAGE_EXTENSIONS,
)

from services.detector import detector


# ============================================================
# BLUEPRINT
# ============================================================

prediction_bp = Blueprint(
    "prediction",
    __name__,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def is_allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has an
    allowed image extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


def create_safe_filename(
    original_filename: str
) -> str:
    """
    Create a unique and secure filename.

    Example:
        car.jpg
        becomes:
        a1b2c3d4_car.jpg
    """

    safe_name = secure_filename(
        original_filename
    )

    unique_id = uuid4().hex[:12]

    return f"{unique_id}_{safe_name}"


# ============================================================
# VEHICLE DAMAGE PREDICTION
# ============================================================

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():
    """
    Receive an image and perform
    vehicle damage detection.

    Endpoint:
        POST /api/predict

    Form field:
        file

    Returns:
        JSON prediction results.
    """

    try:

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "error": "No file uploaded.",
                "message": (
                    "Please select a vehicle image "
                    "and try again."
                ),
            }), 400


        uploaded_file = request.files["file"]


        if uploaded_file.filename == "":

            return jsonify({
                "success": False,
                "error": "No file selected.",
                "message": (
                    "Please select a valid vehicle image."
                ),
            }), 400


        # ----------------------------------------------------
        # VALIDATE FILE TYPE
        # ----------------------------------------------------

        if not is_allowed_file(
            uploaded_file.filename
        ):

            allowed_types = ", ".join(
                sorted(
                    ALLOWED_IMAGE_EXTENSIONS
                )
            )

            return jsonify({
                "success": False,
                "error": "Unsupported file type.",
                "message": (
                    f"Allowed image formats: "
                    f"{allowed_types}"
                ),
            }), 400


        # ----------------------------------------------------
        # CREATE SECURE UNIQUE FILENAME
        # ----------------------------------------------------

        filename = create_safe_filename(
            uploaded_file.filename
        )


        # ----------------------------------------------------
        # CREATE UPLOAD DIRECTORY
        # ----------------------------------------------------

        upload_directory = Path(
            UPLOAD_FOLDER
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        # ----------------------------------------------------
        # SAVE UPLOADED IMAGE
        # ----------------------------------------------------

        image_path = (
            upload_directory / filename
        )


        uploaded_file.save(
            str(image_path)
        )


        # ----------------------------------------------------
        # RUN YOLO26 PREDICTION
        # ----------------------------------------------------

        result = detector.predict(
            image_path
        )


        # ----------------------------------------------------
        # ADD ORIGINAL FILENAME
        # ----------------------------------------------------

        result["original_filename"] = (
            uploaded_file.filename
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify(
            result
        ), 200


    # ========================================================
    # FILE NOT FOUND
    # ========================================================

    except FileNotFoundError as error:

        return jsonify({
            "success": False,
            "error": "File not found.",
            "message": str(error),
        }), 404


    # ========================================================
    # VALUE ERROR
    # ========================================================

    except ValueError as error:

        return jsonify({
            "success": False,
            "error": "Invalid request.",
            "message": str(error),
        }), 400


    # ========================================================
    # GENERAL PREDICTION ERROR
    # ========================================================

    except RuntimeError as error:

        return jsonify({
            "success": False,
            "error": "Prediction failed.",
            "message": str(error),
        }), 500


    # ========================================================
    # UNEXPECTED ERROR
    # ========================================================

    except Exception as error:

        print(
            f"Unexpected prediction error: {error}"
        )

        return jsonify({
            "success": False,
            "error": "Internal server error.",
            "message": (
                "An unexpected error occurred "
                "while processing the image."
            ),
        }), 500