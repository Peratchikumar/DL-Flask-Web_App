import os
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from ultralytics import YOLO


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Maximum upload size: 50 MB
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "uploads"
RESULT_FOLDER = BASE_DIR / "results"

UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULT_FOLDER.mkdir(exist_ok=True)


# ============================================================
# YOLO MODEL
# ============================================================

MODEL_PATH = BASE_DIR / "vehicle_damage_yolo26_best.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}\n"
        "Place vehicle_damage_yolo26_best.pt in the same folder as app.py."
    )

model = YOLO(str(MODEL_PATH))


# ============================================================
# VEHICLE DAMAGE CLASSES
# ============================================================

CLASS_NAMES = [
    "Front-windscreen-damage",
    "Headlight-damage",
    "Rear-windscreen-Damage",
    "Runningboard-Damage",
    "Sidemirror-Damage",
    "Taillight-Damage",
    "bonnet-dent",
    "boot-dent",
    "doorouter-dent",
    "fender-dent",
    "front-bumper-dent",
    "quaterpanel-dent",
    "rear-bumper-dent",
    "roof-dent"
]


# ============================================================
# ALLOWED IMAGE EXTENSIONS
# ============================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp"
}


def allowed_file(filename):
    """Check whether uploaded file has an allowed extension."""

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# IMAGE PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    # --------------------------------------------------------
    # Check whether file exists
    # --------------------------------------------------------

    if "file" not in request.files:

        return render_template(
            "index.html",
            error="Please select an image."
        )


    file = request.files["file"]


    # --------------------------------------------------------
    # Check filename
    # --------------------------------------------------------

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )


    # --------------------------------------------------------
    # Validate file extension
    # --------------------------------------------------------

    if not allowed_file(file.filename):

        return render_template(
            "index.html",
            error="Invalid file type. Please upload JPG, JPEG, PNG, WEBP or BMP."
        )


    # --------------------------------------------------------
    # Save uploaded image
    # --------------------------------------------------------

    filename = secure_filename(file.filename)

    input_path = UPLOAD_FOLDER / filename

    file.save(str(input_path))


    # --------------------------------------------------------
    # Run YOLO prediction
    #
    # Your notebook uses:
    # conf=0.4
    # imgsz=320
    # --------------------------------------------------------

    results = model.predict(
        source=str(input_path),
        conf=0.40,
        imgsz=320,
        save=False,
        verbose=False
    )


    result = results[0]


    # --------------------------------------------------------
    # Save annotated image
    # --------------------------------------------------------

    annotated_image = result.plot()

    output_filename = f"result_{filename}"

    output_path = RESULT_FOLDER / output_filename

    # Save annotated image
    import cv2

    cv2.imwrite(
        str(output_path),
        annotated_image
    )


    # ========================================================
    # EXTRACT DETECTIONS
    # ========================================================

    detections = []


    if result.boxes is not None:

        for box in result.boxes:

            # Class ID
            class_id = int(box.cls[0])

            # Confidence
            confidence = float(box.conf[0])

            # Class name
            if class_id < len(CLASS_NAMES):
                class_name = CLASS_NAMES[class_id]
            else:
                class_name = result.names[class_id]


            detections.append({
                "class": class_name,
                "confidence": round(confidence * 100, 2)
            })


    # ========================================================
    # REMOVE DUPLICATE DAMAGE TYPES
    # ========================================================

    unique_damages = []

    seen = set()

    for detection in detections:

        damage_name = detection["class"]

        if damage_name not in seen:

            unique_damages.append(detection)

            seen.add(damage_name)


    # ========================================================
    # DAMAGE COUNT
    # ========================================================

    damage_count = len(detections)


    # ========================================================
    # RESULT
    # ========================================================

    return render_template(
        "result.html",
        image_filename=output_filename,
        detections=detections,
        unique_damages=unique_damages,
        damage_count=damage_count
    )


# ============================================================
# SERVE RESULT IMAGES
# ============================================================

@app.route("/results/<filename>")
def result_file(filename):

    return send_from_directory(
        RESULT_FOLDER,
        filename
    )


# ============================================================
# SERVE UPLOADED IMAGES
# ============================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# ============================================================
# ERROR HANDLING
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 50 MB."
    ), 413


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )