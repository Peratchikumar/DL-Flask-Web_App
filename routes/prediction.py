"""
Prediction API Routes
Vehicle Damage Detection
YOLO26 + Flask
"""

from pathlib import Path

from flask import Blueprint, jsonify, request

from config.settings import (
    ALLOWED_IMAGE_EXTENSIONS,
    UPLOAD_FOLDER,
)

from services.detector import detector

from utils.file_utils import (
    create_unique_filename,
)


# ============================================================
# BLUEPRINT
# ============================================================

prediction_bp = Blueprint(
    "prediction",
    __name__,
)


# ============================================================
# FILE VALIDATION
# ============================================================

def is_allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has an allowed
    image extension.
    """

    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


# ============================================================
# CONVERT YOLO RESULTS TO JSON
# ============================================================

def format_predictions(results) -> list:
    """
    Convert YOLO prediction results into
    JSON-serializable dictionaries.
    """

    detections = []

    if not results:
        return detections

    result = results[0]

    if result.boxes is None:
        return detections

    names = result.names

    for box in result.boxes:

        class_id = int(
            box.cls[0].item()
        )

        confidence = float(
            box.conf[0].item()
        )

        coordinates = (
            box.xyxy[0]
            .cpu()
            .tolist()
        )

        detections.append({
            "class_id": class_id,
            "class_name": names.get(
                class_id,
                str(class_id)
            ),
            "confidence": round(
                confidence,
                4
            ),
            "confidence_percent": round(
                confidence * 100,
                2
            ),
            "bounding_box": {
                "x1": round(
                    coordinates[0],
                    2
                ),
                "y1": round(
                    coordinates[1],
                    2
                ),
                "x2": round(
                    coordinates[2],
                    2
                ),
                "y2": round(
                    coordinates[3],
                    2
                ),
            },
        })

    return detections


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():
    """
    Vehicle damage prediction endpoint.

    Endpoint:
        POST /api/predict

    Form field:
        file
    """

    image_path = None

    try:

        # ----------------------------------------------------
        # CHECK FILE FIELD
        # ----------------------------------------------------

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "error": "No file uploaded.",
                "message": (
                    "Please select a vehicle image."
                ),
            }), 400


        uploaded_file = request.files["file"]


        # ----------------------------------------------------
        # CHECK FILENAME
        # ----------------------------------------------------

        if not uploaded_file.filename:

            return jsonify({
                "success": False,
                "error": "No file selected.",
                "message": (
                    "Please select a valid image."
                ),
            }), 400


        original_filename = (
            uploaded_file.filename
        )


        # ----------------------------------------------------
        # VALIDATE EXTENSION
        # ----------------------------------------------------

        if not is_allowed_file(
            original_filename
        ):

            allowed = ", ".join(
                sorted(
                    ALLOWED_IMAGE_EXTENSIONS
                )
            )

            return jsonify({
                "success": False,
                "error": "Unsupported file type.",
                "message": (
                    f"Allowed formats: {allowed}"
                ),
            }), 400


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
        # CREATE UNIQUE FILE NAME
        # ----------------------------------------------------

        filename = create_unique_filename(
            original_filename
        )


        image_path = (
            upload_directory / filename
        )


        # ----------------------------------------------------
        # SAVE IMAGE
        # ----------------------------------------------------

        uploaded_file.save(
            str(image_path)
        )


        # ----------------------------------------------------
        # RUN YOLO26
        # ----------------------------------------------------

        results = detector.predict(
            source=image_path
        )


        # ----------------------------------------------------
        # FORMAT RESULTS
        # ----------------------------------------------------

        detections = format_predictions(
            results
        )


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "original_filename": (
                original_filename
            ),
            "filename": filename,
            "detection_count": len(
                detections
            ),
            "detections": detections,
        }), 200


    # ========================================================
    # FILE ERROR
    # ========================================================

    except FileNotFoundError as error:

        return jsonify({
            "success": False,
            "error": "File not found.",
            "message": str(error),
        }), 404


    # ========================================================
    # PREDICTION ERROR
    # ========================================================

    except RuntimeError as error:

        return jsonify({
            "success": False,
            "error": "Prediction failed.",
            "message": str(error),
        }), 500


    # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as error:

        print(
            f"Prediction error: {error}"
        )

        return jsonify({
            "success": False,
            "error": "Internal server error.",
            "message": (
                "An unexpected error occurred "
                "while processing the image."
            ),
        }), 500