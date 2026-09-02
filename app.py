import os
import uuid
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_from_directory
)

from werkzeug.utils import secure_filename
from ultralytics import YOLO


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# APPLICATION SETTINGS
# =========================================================

MAX_FILE_SIZE = 100 * 1024 * 1024

app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "vehicle_damage_yolo26_best.pt"

UPLOAD_FOLDER = BASE_DIR / "uploads"

RESULT_FOLDER = BASE_DIR / "results"


UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

RESULT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# IMAGE FILE TYPES ONLY
# =========================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp"
}


def allowed_file(filename):
    """
    Check whether the uploaded file
    has an allowed image extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# =========================================================
# LOAD YOLO26 MODEL
# =========================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"\nYOLO26 model not found:\n"
        f"{MODEL_PATH}\n\n"
        f"Place vehicle_damage_yolo26_best.pt "
        f"inside the project folder."
    )


model = YOLO(
    str(MODEL_PATH)
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# PREDICTION ENDPOINT
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # -----------------------------------------------------
    # CHECK FILE FIELD
    # -----------------------------------------------------

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "error": "No image was uploaded."
        }), 400


    file = request.files["file"]


    # -----------------------------------------------------
    # CHECK EMPTY FILE
    # -----------------------------------------------------

    if not file or file.filename == "":

        return jsonify({
            "success": False,
            "error": "Please select a vehicle image."
        }), 400


    # -----------------------------------------------------
    # CHECK EXTENSION
    # -----------------------------------------------------

    if not allowed_file(file.filename):

        return jsonify({
            "success": False,
            "error": (
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, WEBP, or BMP."
            )
        }), 400


    # -----------------------------------------------------
    # SECURE ORIGINAL FILENAME
    # -----------------------------------------------------

    original_name = secure_filename(
        file.filename
    )


    if not original_name:

        return jsonify({
            "success": False,
            "error": "Invalid filename."
        }), 400


    # -----------------------------------------------------
    # FILE EXTENSION
    # -----------------------------------------------------

    extension = Path(
        original_name
    ).suffix.lower()


    # -----------------------------------------------------
    # UNIQUE ID
    # -----------------------------------------------------

    unique_id = uuid.uuid4().hex


    # -----------------------------------------------------
    # SAVE INPUT IMAGE
    # -----------------------------------------------------

    input_filename = (
        f"{unique_id}{extension}"
    )

    input_path = (
        UPLOAD_FOLDER /
        input_filename
    )


    try:

        file.save(
            str(input_path)
        )

    except Exception as error:

        return jsonify({
            "success": False,
            "error": (
                f"Could not save uploaded image: "
                f"{str(error)}"
            )
        }), 500


    # -----------------------------------------------------
    # CREATE RESULT DIRECTORY
    # -----------------------------------------------------

    result_name = unique_id

    result_path = (
        RESULT_FOLDER /
        result_name
    )

    result_path.mkdir(
        parents=True,
        exist_ok=True
    )


    # =====================================================
    # YOLO26 INFERENCE
    # =====================================================

    try:

        results = model.predict(

            source=str(input_path),

            conf=0.25,

            imgsz=320,

            save=True,

            project=str(
                RESULT_FOLDER
            ),

            name=result_name,

            exist_ok=True
        )

    except Exception as error:

        try:
            input_path.unlink(
                missing_ok=True
            )
        except Exception:
            pass

        return jsonify({
            "success": False,
            "error": (
                f"Detection failed: "
                f"{str(error)}"
            )
        }), 500


    # =====================================================
    # FIND OUTPUT IMAGE
    # =====================================================

    output_files = list(
        result_path.iterdir()
    )


    if not output_files:

        return jsonify({
            "success": False,
            "error": (
                "Detection completed, "
                "but no output image was generated."
            )
        }), 500


    output_file = None


    for item in output_files:

        if item.is_file():

            output_file = item

            if (
                item.suffix.lower()
                == extension
            ):
                break


    if output_file is None:

        return jsonify({
            "success": False,
            "error": (
                "Could not find the "
                "detection result image."
            )
        }), 500


    # =====================================================
    # COLLECT DETECTIONS
    # =====================================================

    detections = []


    try:

        for result in results:

            if result.boxes is None:
                continue


            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )


                class_name = model.names.get(
                    class_id,
                    str(class_id)
                )


                detections.append({

                    "class": class_name,

                    "confidence": round(
                        confidence * 100,
                        2
                    )
                })


    except Exception:

        detections = []


    # =====================================================
    # DAMAGE COUNTS
    # =====================================================

    damage_counts = {}


    for detection in detections:

        class_name = (
            detection["class"]
        )

        damage_counts[class_name] = (
            damage_counts.get(
                class_name,
                0
            ) + 1
        )


    # =====================================================
    # AVERAGE CONFIDENCE
    # =====================================================

    if detections:

        average_confidence = round(

            sum(
                detection["confidence"]
                for detection in detections
            )
            /
            len(detections),

            2
        )

    else:

        average_confidence = 0.0


    # =====================================================
    # RESULT URL
    # =====================================================

    result_url = (
        f"/results/"
        f"{result_name}/"
        f"{output_file.name}"
    )


    # =====================================================
    # RESPONSE
    # =====================================================

    return jsonify({

        "success": True,

        "message": (
            "Vehicle damage detection "
            "completed successfully."
        ),

        "filename": original_name,

        "media_type": "image",

        "result_url": result_url,

        "total_detections": len(
            detections
        ),

        "average_confidence": (
            average_confidence
        ),

        "damage_counts": (
            damage_counts
        ),

        "detections": detections
    })


# =========================================================
# SERVE RESULT IMAGE
# =========================================================

@app.route(
    "/results/<result_name>/<filename>"
)
def serve_result(
    result_name,
    filename
):

    result_directory = (
        RESULT_FOLDER /
        result_name
    )


    return send_from_directory(
        str(result_directory),
        filename
    )


# =========================================================
# FILE TOO LARGE
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "error": (
            "File is too large. "
            "Maximum size is 100 MB."
        )

    }), 413


# =========================================================
# 404
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "error": "Page not found."

    }), 404


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),

        debug=True
    )