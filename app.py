import os
import uuid
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

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


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
# HELPER FUNCTION
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


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
    # SAVE UPLOADED IMAGE
    # --------------------------------------------------------

    original_filename = secure_filename(
        file.filename
    )

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

    file.save(upload_path)


    print("=" * 60)
    print("New prediction request")
    print(f"Input image: {upload_path}")
    print("=" * 60)


    try:

        # ----------------------------------------------------
        # RUN YOLO
        # ----------------------------------------------------

        results = model.predict(
            source=upload_path,
            conf=0.25,
            iou=0.45,
            imgsz=640,
            verbose=False
        )

        result = results[0]


        # ----------------------------------------------------
        # CREATE ANNOTATED IMAGE
        # ----------------------------------------------------

        annotated_image = result.plot()


        # ----------------------------------------------------
        # SAVE RESULT INTO STATIC/RESULTS
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
            annotated_image
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

            for i in range(
                len(result.boxes)
            ):

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
            "Maximum size is 16 MB."
        )

    }), 413


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )