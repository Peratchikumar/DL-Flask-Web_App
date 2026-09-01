import os
from pathlib import Path

import cv2
from flask import Flask, render_template, request, send_from_directory
from ultralytics import YOLO
from werkzeug.utils import secure_filename


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "vehicle_damage_yolo26_best.pt"
)

UPLOAD_FOLDER = BASE_DIR / "uploads"

OUTPUT_FOLDER = BASE_DIR / "outputs"


# Create folders if they do not exist
UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

app.config["OUTPUT_FOLDER"] = str(OUTPUT_FOLDER)

# Maximum upload size = 50 MB
app.config["MAX_CONTENT_LENGTH"] = (
    50 * 1024 * 1024
)


# ============================================================
# ALLOWED IMAGE FORMATS
# ============================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp"
}


# ============================================================
# VEHICLE DAMAGE CLASS NAMES
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
# CHECK MODEL FILE
# ============================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"\nModel file not found:\n"
        f"{MODEL_PATH}\n\n"
        f"Expected location:\n"
        f"model/vehicle_damage_yolo26_best.pt\n"
    )


# ============================================================
# LOAD YOLO MODEL
# ============================================================

print(
    f"Loading YOLO model from: {MODEL_PATH}"
)

model = YOLO(
    str(MODEL_PATH)
)

print(
    "Vehicle Damage Detection model loaded successfully."
)


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename
        .rsplit(".", 1)[1]
        .lower()
        in ALLOWED_EXTENSIONS
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
# VEHICLE DAMAGE PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # Check file input
    # --------------------------------------------------------

    if "file" not in request.files:

        return render_template(
            "index.html",
            error="Please select an image."
        )


    file = request.files["file"]


    # --------------------------------------------------------
    # Check empty filename
    # --------------------------------------------------------

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )


    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    if not allowed_file(
        file.filename
    ):

        return render_template(
            "index.html",
            error=(
                "Invalid file type. "
                "Please upload JPG, JPEG, "
                "PNG, WEBP or BMP."
            )
        )


    # --------------------------------------------------------
    # Secure filename
    # --------------------------------------------------------

    filename = secure_filename(
        file.filename
    )


    # --------------------------------------------------------
    # Save uploaded image
    # --------------------------------------------------------

    input_path = (
        UPLOAD_FOLDER
        / filename
    )


    file.save(
        str(input_path)
    )


    try:

        # ====================================================
        # RUN YOLO DETECTION
        # ====================================================

        results = model.predict(
            source=str(input_path),
            conf=0.40,
            imgsz=320,
            save=False,
            verbose=False
        )


        result = results[0]


        # ====================================================
        # CREATE ANNOTATED IMAGE
        # ====================================================

        annotated_image = (
            result.plot()
        )


        # ----------------------------------------------------
        # Output filename
        # ----------------------------------------------------

        output_filename = (
            f"result_{filename}"
        )


        output_path = (
            OUTPUT_FOLDER
            / output_filename
        )


        # ----------------------------------------------------
        # Save output image
        # ----------------------------------------------------

        success = cv2.imwrite(
            str(output_path),
            annotated_image
        )


        if not success:

            raise RuntimeError(
                "Failed to save processed image."
            )


        # ====================================================
        # EXTRACT DETECTIONS
        # ====================================================

        detections = []


        if (
            result.boxes
            is not None
        ):

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )


                confidence = float(
                    box.conf[0]
                )


                # --------------------------------------------
                # Get class name
                # --------------------------------------------

                if (
                    class_id
                    <
                    len(CLASS_NAMES)
                ):

                    class_name = (
                        CLASS_NAMES[
                            class_id
                        ]
                    )

                else:

                    class_name = (
                        result.names[
                            class_id
                        ]
                    )


                # --------------------------------------------
                # Bounding box coordinates
                # --------------------------------------------

                coordinates = (
                    box.xyxy[0]
                    .cpu()
                    .tolist()
                )


                x1, y1, x2, y2 = (
                    coordinates
                )


                detections.append({
                    "class":
                        class_name,

                    "confidence":
                        round(
                            confidence
                            * 100,
                            2
                        ),

                    "box": {
                        "x1":
                            round(x1, 2),

                        "y1":
                            round(y1, 2),

                        "x2":
                            round(x2, 2),

                        "y2":
                            round(y2, 2)
                    }
                })


        # ====================================================
        # UNIQUE DAMAGE TYPES
        # ====================================================

        unique_damages = []

        seen_classes = set()


        for detection in detections:

            damage_class = (
                detection["class"]
            )


            if (
                damage_class
                not in seen_classes
            ):

                unique_damages.append(
                    detection
                )

                seen_classes.add(
                    damage_class
                )


        # ====================================================
        # DAMAGE COUNT
        # ====================================================

        damage_count = len(
            detections
        )


        # ====================================================
        # SHOW RESULT PAGE
        # ====================================================

        return render_template(
            "result.html",

            image_filename=
                output_filename,

            detections=
                detections,

            unique_damages=
                unique_damages,

            damage_count=
                damage_count
        )


    except Exception as error:

        print(
            f"Prediction error: {error}"
        )


        return render_template(
            "index.html",
            error=(
                "An error occurred while "
                "processing the image. "
                "Please try again."
            )
        )


# ============================================================
# SERVE OUTPUT IMAGES
# ============================================================

@app.route(
    "/outputs/<filename>"
)
def result_file(filename):

    return send_from_directory(
        str(OUTPUT_FOLDER),
        filename
    )


# ============================================================
# SERVE UPLOADED IMAGES
# ============================================================

@app.route(
    "/uploads/<filename>"
)
def uploaded_file(filename):

    return send_from_directory(
        str(UPLOAD_FOLDER),
        filename
    )


# ============================================================
# FILE TOO LARGE ERROR
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error=(
            "The uploaded file is too large. "
            "Maximum allowed size is 50 MB."
        )
    ), 413


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "404 - Page Not Found",
        404
    )


# ============================================================
# RUN APPLICATION
# ============================================================

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