import os
import uuid
import gc
import threading

import cv2

from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from ultralytics import YOLO


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# PATHS
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vehicle_damage_yolo26_best.pt"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

RESULT_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "results"
)


# ============================================================
# CONFIGURATION
# ============================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

# Limit uploaded file size to 8 MB
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

# Render should use only one inference request at a time
# to prevent multiple YOLO predictions consuming RAM.
prediction_lock = threading.Lock()


# ============================================================
# CREATE FOLDERS
# ============================================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

print("=" * 60)
print("Loading Vehicle Damage Detection Model...")
print("=" * 60)

model = YOLO(MODEL_PATH)

print("Model loaded successfully!")
print("Classes:")

for class_id, class_name in model.names.items():
    print(f"  {class_id}: {class_name}")

print("=" * 60)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def cleanup_memory():
    """
    Release unused Python memory after each prediction.
    """
    gc.collect()


def resize_image_for_inference(image, max_dimension=1280):
    """
    Reduce very large uploaded images before sending them
    to YOLO. This helps reduce RAM usage on Render.
    """

    height, width = image.shape[:2]

    largest_dimension = max(height, width)

    if largest_dimension <= max_dimension:
        return image

    scale = max_dimension / largest_dimension

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    return resized


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image was uploaded."
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select an image."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": (
                "Invalid image format. "
                "Use JPG, JPEG, PNG or WEBP."
            )
        }), 400


    # --------------------------------------------------------
    # GENERATE UNIQUE FILE NAME
    # --------------------------------------------------------

    original_filename = secure_filename(file.filename)

    extension = original_filename.rsplit(
        ".",
        1
    )[1].lower()

    unique_id = uuid.uuid4().hex

    upload_filename = (
        f"{unique_id}_input.{extension}"
    )

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        upload_filename
    )


    # --------------------------------------------------------
    # SAVE UPLOADED IMAGE
    # --------------------------------------------------------

    file.save(upload_path)

    print("=" * 60)
    print("New prediction request")
    print(f"Input image: {upload_path}")
    print("=" * 60)


    # --------------------------------------------------------
    # PREVENT MULTIPLE YOLO REQUESTS
    # --------------------------------------------------------

    acquired = prediction_lock.acquire(
        timeout=120
    )

    if not acquired:
        return jsonify({
            "success": False,
            "error": (
                "The AI model is currently busy. "
                "Please try again in a moment."
            )
        }), 503


    image = None
    resized_image = None
    result = None
    annotated_image = None

    try:

        # ----------------------------------------------------
        # READ IMAGE WITH OPENCV
        # ----------------------------------------------------

        image = cv2.imread(upload_path)

        if image is None:
            raise RuntimeError(
                "Could not read the uploaded image."
            )


        # ----------------------------------------------------
        # REDUCE LARGE IMAGE MEMORY
        # ----------------------------------------------------

        resized_image = resize_image_for_inference(
            image,
            max_dimension=1280
        )


        # ----------------------------------------------------
        # RUN YOLO
        # ----------------------------------------------------
        #
        # Important memory optimizations:
        #
        # imgsz=416 instead of 640
        # device=cpu
        # batch=1
        # stream=True
        #
        # ----------------------------------------------------

        results_generator = model.predict(
            source=resized_image,
            conf=0.25,
            iou=0.45,
            imgsz=416,
            device="cpu",
            batch=1,
            stream=True,
            verbose=False
        )

        # Get only the first result instead of creating
        # a complete results list.
        result = next(results_generator)


        # ----------------------------------------------------
        # CREATE ANNOTATED IMAGE
        # ----------------------------------------------------

        annotated_image = result.plot()


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        result_filename = (
            f"{unique_id}_result.jpg"
        )

        result_path = os.path.join(
            RESULT_FOLDER,
            result_filename
        )

        success = cv2.imwrite(
            result_path,
            annotated_image,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                90
            ]
        )

        if not success:
            raise RuntimeError(
                "Could not save annotated result image."
            )

        print(
            f"Result image saved: {result_path}"
        )


        # ----------------------------------------------------
        # EXTRACT DETECTIONS
        # ----------------------------------------------------

        detections = []

        if result.boxes is not None:

            for i in range(len(result.boxes)):

                class_id = int(
                    result.boxes.cls[i].item()
                )

                confidence = float(
                    result.boxes.conf[i].item()
                )

                coordinates = (
                    result.boxes.xyxy[i]
                    .tolist()
                )

                class_name = model.names[
                    class_id
                ]

                detections.append({

                    "class_id": class_id,

                    "class_name": class_name,

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
                        )
                    }
                })


        # ----------------------------------------------------
        # CREATE BROWSER URL
        # ----------------------------------------------------

        result_url = url_for(
            "static",
            filename=(
                f"results/{result_filename}"
            )
        )

        print(
            f"Browser result URL: {result_url}"
        )

        print(
            f"Detections: {len(detections)}"
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "message": (
                "Vehicle damage detection "
                "completed successfully."
            ),

            "detection_count": len(
                detections
            ),

            "detections": detections,

            "result_image": result_url

        })


    except Exception as error:

        print("=" * 60)
        print("PREDICTION ERROR")
        print(error)
        print("=" * 60)

        return jsonify({

            "success": False,

            "error": (
                "Vehicle damage detection failed."
            ),

            "details": str(error)

        }), 500


    finally:

        # ----------------------------------------------------
        # RELEASE MEMORY
        # ----------------------------------------------------

        try:
            del results_generator
        except Exception:
            pass

        image = None
        resized_image = None
        result = None
        annotated_image = None

        cleanup_memory()

        prediction_lock.release()


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "model": (
            "vehicle_damage_yolo26_best.pt"
        ),

        "classes": model.names

    })


# ============================================================
# FILE SIZE ERROR
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "error": (
            "Image is too large. "
            "Maximum size is 8 MB."
        )

    }), 413


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False,
        use_reloader=False
    )