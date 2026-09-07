import os
import gc
import uuid
import traceback
from pathlib import Path

import cv2
import torch
from PIL import Image
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO


# ============================================================
# DRIVEINSPECT — LOW-MEMORY FLASK + YOLO26 DEPLOYMENT
# ============================================================

app = Flask(__name__)

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "vehicle_damage_yolo26_best.pt"
UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULT_FOLDER = BASE_DIR / "results"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Application settings
# ------------------------------------------------------------

app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp",
}


# ------------------------------------------------------------
# Load YOLO26 model ONCE
# ------------------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO26 model not found: {MODEL_PATH}"
    )

print(f"Loading YOLO26 model from: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))

print("YOLO26 model loaded successfully.")


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def allowed_file(filename):
    """Check whether the uploaded file has a supported extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def create_safe_filename(filename):
    """Create a safe unique filename."""

    original_name = secure_filename(filename)

    if not original_name:
        original_name = "vehicle.jpg"

    extension = Path(original_name).suffix.lower()

    if extension not in {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
    }:
        extension = ".jpg"

    unique_name = f"{uuid.uuid4().hex}{extension}"

    return unique_name


def prepare_image(input_path):
    """
    Resize large images before YOLO inference.

    This reduces memory usage on low-memory hosting platforms.
    """

    image = Image.open(input_path)

    # Convert to RGB.
    image = image.convert("RGB")

    # Maximum working image dimension.
    max_dimension = 1280

    if max(image.size) > max_dimension:
        image.thumbnail(
            (max_dimension, max_dimension),
            Image.Resampling.LANCZOS
        )

    prepared_name = f"{uuid.uuid4().hex}_prepared.jpg"

    prepared_path = UPLOAD_FOLDER / prepared_name

    image.save(
        prepared_path,
        format="JPEG",
        quality=90,
        optimize=True
    )

    image.close()

    return prepared_path


def cleanup_file(path):
    """Safely delete a temporary file."""

    try:

        if path and Path(path).exists():
            Path(path).unlink()

    except Exception:

        traceback.print_exc()


# ------------------------------------------------------------
# Home
# ------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")


# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    input_path = None
    prepared_path = None

    try:

        # ----------------------------------------------------
        # Validate uploaded file
        # ----------------------------------------------------

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "message": "No image file was uploaded."
            }), 400

        file = request.files["file"]

        if not file or not file.filename:

            return jsonify({
                "success": False,
                "message": "No image was selected."
            }), 400

        if not allowed_file(file.filename):

            return jsonify({
                "success": False,
                "message": (
                    "Unsupported image format. "
                    "Use JPG, JPEG, PNG, WEBP, or BMP."
                )
            }), 400

        # ----------------------------------------------------
        # Save uploaded image
        # ----------------------------------------------------

        safe_filename = create_safe_filename(
            file.filename
        )

        input_path = UPLOAD_FOLDER / safe_filename

        file.save(input_path)

        print(
            f"Uploaded image saved to: {input_path}"
        )

        # ----------------------------------------------------
        # Prepare memory-friendly image
        # ----------------------------------------------------

        prepared_path = prepare_image(
            input_path
        )

        print(
            f"Prepared image saved to: {prepared_path}"
        )

        # ----------------------------------------------------
        # Create result directory
        # ----------------------------------------------------

        result_name = uuid.uuid4().hex

        result_dir = RESULT_FOLDER / result_name

        result_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        result_filename = "result.jpg"

        result_path = result_dir / result_filename

        # ----------------------------------------------------
        # YOLO26 inference
        # ----------------------------------------------------

        print("Starting YOLO26 inference...")

        with torch.inference_mode():

            predictions = model.predict(
                source=str(prepared_path),
                conf=0.25,
                imgsz=256,
                device="cpu",
                max_det=20,
                verbose=False,
                save=False
            )

        print("YOLO26 inference completed.")

        # ----------------------------------------------------
        # Validate prediction result
        # ----------------------------------------------------

        if not predictions:

            return jsonify({
                "success": False,
                "message": (
                    "The model returned no prediction result."
                )
            }), 500

        prediction = predictions[0]

        # ----------------------------------------------------
        # Detection information
        # ----------------------------------------------------

        detections = []

        damage_counts = {}

        if (
            prediction.boxes is not None
            and len(prediction.boxes) > 0
        ):

            class_ids = (
                prediction.boxes.cls
                .cpu()
                .tolist()
            )

            confidences = (
                prediction.boxes.conf
                .cpu()
                .tolist()
            )

            for class_id, confidence in zip(
                class_ids,
                confidences
            ):

                class_id = int(class_id)

                confidence_percent = (
                    float(confidence) * 100.0
                )

                class_name = prediction.names.get(
                    class_id,
                    str(class_id)
                )

                detections.append({
                    "class": class_name,
                    "confidence": round(
                        confidence_percent,
                        2
                    )
                })

                damage_counts[class_name] = (
                    damage_counts.get(
                        class_name,
                        0
                    ) + 1
                )

        # ----------------------------------------------------
        # Calculate statistics
        # ----------------------------------------------------

        total_detections = len(
            detections
        )

        if total_detections > 0:

            average_confidence = (
                sum(
                    item["confidence"]
                    for item in detections
                )
                / total_detections
            )

        else:

            average_confidence = 0.0

        # ----------------------------------------------------
        # Generate annotated image
        # ----------------------------------------------------

        print(
            "Generating annotated result image..."
        )

        annotated_image = prediction.plot(
            conf=True,
            labels=True,
            boxes=True
        )

        # ----------------------------------------------------
        # Save annotated image
        # ----------------------------------------------------

        success = cv2.imwrite(
            str(result_path),
            annotated_image,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                90
            ]
        )

        if not success:

            raise RuntimeError(
                "Failed to save the annotated result image."
            )

        print(
            f"Result image saved to: {result_path}"
        )

        # ----------------------------------------------------
        # Release memory
        # ----------------------------------------------------

        del annotated_image
        del predictions
        del prediction

        gc.collect()

        # ----------------------------------------------------
        # Return JSON response
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "message": (
                "Vehicle damage detection "
                "completed successfully."
            ),
            "filename": file.filename,
            "media_type": "image",
            "result_url": (
                f"/results/"
                f"{result_name}/"
                f"{result_filename}"
            ),
            "total_detections": total_detections,
            "average_confidence": round(
                average_confidence,
                2
            ),
            "damage_counts": damage_counts,
            "detections": detections
        })

    except Exception as exc:

        # ----------------------------------------------------
        # IMPORTANT:
        # Print complete traceback to Render logs.
        # ----------------------------------------------------

        print("=" * 70)

        print("YOLO26 PREDICTION ERROR")

        print("=" * 70)

        print(
            f"Exception type: {type(exc).__name__}"
        )

        print(
            f"Exception message: {exc}"
        )

        print(
            "\nComplete traceback:"
        )

        traceback.print_exc()

        print("=" * 70)

        return jsonify({
            "success": False,
            "message": (
                "Detection failed: "
                f"{str(exc)}"
            )
        }), 500

    finally:

        # ----------------------------------------------------
        # Delete temporary prepared image
        # ----------------------------------------------------

        cleanup_file(
            prepared_path
        )

        # ----------------------------------------------------
        # Delete uploaded source image
        # ----------------------------------------------------

        cleanup_file(
            input_path
        )

        # ----------------------------------------------------
        # Force garbage collection
        # ----------------------------------------------------

        gc.collect()


# ------------------------------------------------------------
# Serve detection results
# ------------------------------------------------------------

@app.route(
    "/results/<result_name>/<filename>",
    methods=["GET"]
)
def serve_result(
    result_name,
    filename
):

    result_directory = (
        RESULT_FOLDER
        / secure_filename(result_name)
    )

    return send_from_directory(
        result_directory,
        secure_filename(filename)
    )


# ------------------------------------------------------------
# Error handlers
# ------------------------------------------------------------

@app.errorhandler(413)
def request_too_large(error):

    return jsonify({
        "success": False,
        "message": (
            "The uploaded image is too large. "
            "Maximum size is 100 MB."
        )
    }), 413


@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "success": False,
        "message": (
            "Requested resource was not found."
        )
    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    print("=" * 70)

    print("FLASK INTERNAL SERVER ERROR")

    print("=" * 70)

    traceback.print_exc()

    print("=" * 70)

    return jsonify({
        "success": False,
        "message": "Internal server error."
    }), 500


# ------------------------------------------------------------
# Application startup
# ------------------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )