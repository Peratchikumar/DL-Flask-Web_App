import os
from pathlib import Path

import cv2
import torch

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for
)

from ultralytics import YOLO
from werkzeug.utils import secure_filename


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# DIRECTORIES
# ============================================================

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "vehicle_damage_yolo26_best.pt"
)

UPLOAD_FOLDER = (
    BASE_DIR
    / "uploads"
)

OUTPUT_FOLDER = (
    BASE_DIR
    / "outputs"
)


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

app.config["UPLOAD_FOLDER"] = str(
    UPLOAD_FOLDER
)

app.config["OUTPUT_FOLDER"] = str(
    OUTPUT_FOLDER
)

# Maximum upload size: 20 MB
app.config["MAX_CONTENT_LENGTH"] = (
    20 * 1024 * 1024
)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp"
}


# ============================================================
# DAMAGE CLASSES
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
# PYTORCH MEMORY OPTIMIZATION
# ============================================================

torch.set_num_threads(1)

try:
    torch.set_num_interop_threads(1)
except RuntimeError:
    pass


# ============================================================
# CHECK MODEL
# ============================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Model file not found:\n{MODEL_PATH}"
    )


# ============================================================
# LOAD MODEL
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
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["GET", "POST"]
)
def predict():

    # --------------------------------------------------------
    # Prevent direct GET request
    # --------------------------------------------------------

    if request.method == "GET":

        return redirect(
            url_for("home")
        )


    # --------------------------------------------------------
    # Check uploaded file
    # --------------------------------------------------------

    if "file" not in request.files:

        return render_template(
            "index.html",
            error="Please select a vehicle image."
        )


    file = request.files["file"]


    if not file:

        return render_template(
            "index.html",
            error="Please select a vehicle image."
        )


    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select a vehicle image."
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
                "Invalid image format. "
                "Please use JPG, JPEG, PNG, "
                "WEBP or BMP."
            )
        )


    # --------------------------------------------------------
    # Secure filename
    # --------------------------------------------------------

    filename = secure_filename(
        file.filename
    )


    if not filename:

        return render_template(
            "index.html",
            error="Invalid filename."
        )


    input_path = (
        UPLOAD_FOLDER
        / filename
    )


    try:

        # ====================================================
        # SAVE IMAGE
        # ====================================================

        file.save(
            str(input_path)
        )

        print(
            f"Uploaded image: {input_path}"
        )


        # ====================================================
        # READ IMAGE
        # ====================================================

        image = cv2.imread(
            str(input_path)
        )


        if image is None:

            raise ValueError(
                "Unable to read uploaded image."
            )


        # ====================================================
        # MEMORY OPTIMIZATION
        #
        # Very large photographs can consume significant RAM.
        # Resize them before sending them to YOLO.
        # ====================================================

        max_dimension = 1280

        height, width = (
            image.shape[:2]
        )


        if max(
            height,
            width
        ) > max_dimension:

            scale = (
                max_dimension
                /
                max(
                    height,
                    width
                )
            )


            new_width = int(
                width * scale
            )

            new_height = int(
                height * scale
            )


            image = cv2.resize(
                image,
                (
                    new_width,
                    new_height
                ),
                interpolation=cv2.INTER_AREA
            )


        print(
            f"Inference image size: "
            f"{image.shape[1]}x{image.shape[0]}"
        )


        # ====================================================
        # YOLO INFERENCE
        # ====================================================

        results = model.predict(
            source=image,

            # Reduced image size for low-memory deployment
            imgsz=256,

            # Confidence threshold
            conf=0.40,

            # CPU inference
            device="cpu",

            # Don't save automatically
            save=False,

            # Disable verbose logging
            verbose=False,

            # Single image
            batch=1
        )


        print(
            "YOLO prediction completed."
        )


        # ====================================================
        # GET RESULT
        # ====================================================

        result = results[0]


        # ====================================================
        # CREATE ANNOTATED IMAGE
        # ====================================================

        annotated_image = result.plot(
            line_width=2
        )


        # ====================================================
        # OUTPUT FILE
        # ====================================================

        output_filename = (
            f"result_{filename}"
        )


        output_path = (
            OUTPUT_FOLDER
            / output_filename
        )


        # ====================================================
        # SAVE RESULT
        # ====================================================

        success = cv2.imwrite(
            str(output_path),
            annotated_image
        )


        if not success:

            raise RuntimeError(
                "Failed to save processed image."
            )


        print(
            f"Output saved: {output_path}"
        )


        # ====================================================
        # DETECTIONS
        # ====================================================

        detections = []


        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )


                # --------------------------------------------
                # CLASS NAME
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

                    class_name = str(
                        result.names.get(
                            class_id,
                            "Unknown Damage"
                        )
                    )


                # --------------------------------------------
                # BOX
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
                            confidence * 100,
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


        print(
            f"Detected damage objects: "
            f"{damage_count}"
        )


        # ====================================================
        # RELEASE TEMPORARY OBJECTS
        # ====================================================

        del results

        del result

        del image

        del annotated_image


        # ====================================================
        # RESULT PAGE
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
            "========================================"
        )

        print(
            "PREDICTION ERROR:"
        )

        print(
            repr(error)
        )

        print(
            "========================================"
        )


        return render_template(
            "index.html",

            error=(
                "Vehicle damage detection "
                "failed. Please try another "
                "image."
            )
        )


# ============================================================
# OUTPUT FILES
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
# UPLOADED FILES
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
# FILE TOO LARGE
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error=(
            "Image is too large. "
            "Maximum upload size is 20 MB."
        )
    ), 413


# ============================================================
# 404
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "404 - Page Not Found",
        404
    )


# ============================================================
# APPLICATION START
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