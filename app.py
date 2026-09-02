import os
import base64
from io import BytesIO

from flask import Flask, render_template, request
from PIL import Image
from ultralytics import YOLO


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app = Flask(__name__)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "vehicle_damage_yolo26_best.pt"
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)


OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "outputs"
)


# Create directories if they don't exist
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ============================================================
# ALLOWED IMAGE EXTENSIONS
# ============================================================

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_file(filename):
    """
    Check whether the uploaded file has
    an allowed image extension.
    """

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# LOAD YOLO26 MODEL
# ============================================================

if not os.path.isfile(MODEL_PATH):

    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )


print(
    f"Loading YOLO26 model from: {MODEL_PATH}"
)


model = YOLO(
    MODEL_PATH
)


print(
    "Vehicle Damage Detection model loaded successfully."
)


# ============================================================
# HOME / DETECTION ROUTE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    # --------------------------------------------------------
    # GET REQUEST
    # --------------------------------------------------------

    if request.method == "GET":

        return render_template(
            "index.html",
            result=None
        )


    # --------------------------------------------------------
    # CHECK WHETHER FILE EXISTS
    # --------------------------------------------------------

    if "vehicle_image" not in request.files:

        return render_template(
            "index.html",
            result={
                "success": False,
                "error":
                    "Please select a vehicle image."
            }
        )


    file = request.files[
        "vehicle_image"
    ]


    # --------------------------------------------------------
    # CHECK EMPTY FILE NAME
    # --------------------------------------------------------

    if not file.filename:

        return render_template(
            "index.html",
            result={
                "success": False,
                "error":
                    "No image was selected."
            }
        )


    # --------------------------------------------------------
    # VALIDATE FILE TYPE
    # --------------------------------------------------------

    if not allowed_file(
        file.filename
    ):

        return render_template(
            "index.html",
            result={
                "success": False,
                "error":
                    (
                        "Invalid file type. "
                        "Please upload JPG, JPEG, "
                        "PNG or WEBP."
                    )
            }
        )


    try:

        # ====================================================
        # READ UPLOADED IMAGE
        # ====================================================

        image = Image.open(
            file.stream
        ).convert("RGB")


        # ====================================================
        # RESIZE LARGE IMAGES
        # ====================================================

        max_dimension = 1600


        if max(image.size) > max_dimension:

            resize_ratio = (
                max_dimension /
                max(image.size)
            )


            new_width = int(
                image.width *
                resize_ratio
            )


            new_height = int(
                image.height *
                resize_ratio
            )


            image = image.resize(
                (
                    new_width,
                    new_height
                ),
                Image.LANCZOS
            )


        # ====================================================
        # YOLO26 INFERENCE
        # ====================================================

        results = model.predict(
            source=image,

            # Confidence threshold
            conf=0.25,

            # Image size
            imgsz=640,

            # CPU is safer for low-memory deployment
            device="cpu",

            # Disable verbose prediction logs
            verbose=False
        )


        # Get first prediction result
        prediction = results[0]


        # ====================================================
        # EXTRACT DETECTIONS
        # ====================================================

        detections = []


        if prediction.boxes is not None:

            boxes = prediction.boxes


            for index in range(
                len(boxes)
            ):

                # Confidence
                confidence = float(
                    boxes.conf[
                        index
                    ].item()
                )


                # Class ID
                class_id = int(
                    boxes.cls[
                        index
                    ].item()
                )


                # Class name
                class_name = prediction.names.get(
                    class_id,
                    str(class_id)
                )


                detections.append(
                    {
                        "class":
                            class_name,

                        "confidence":
                            round(
                                confidence * 100,
                                2
                            )
                    }
                )


        # ====================================================
        # UNIQUE DAMAGE TYPES
        # ====================================================

        unique_damage_names = sorted(
            set(
                detection["class"]
                for detection
                in detections
            )
        )


        unique_damages = [

            {
                "class": damage_name
            }

            for damage_name
            in unique_damage_names

        ]


        # ====================================================
        # CREATE ANNOTATED IMAGE
        # ====================================================

        annotated_array = prediction.plot(
            conf=True,
            labels=True,
            boxes=True
        )


        # ====================================================
        # CONVERT ANNOTATED IMAGE
        # TO BROWSER-READY JPEG
        # ====================================================

        # YOLO plot returns a BGR NumPy array.
        # Convert it to RGB for PIL.

        annotated_image = Image.fromarray(
            annotated_array[:, :, ::-1]
        )


        image_buffer = BytesIO()


        annotated_image.save(
            image_buffer,
            format="JPEG",
            quality=88,
            optimize=True
        )


        # ====================================================
        # ENCODE IMAGE AS BASE64
        # ====================================================

        image_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode(
            "utf-8"
        )


        # ====================================================
        # CREATE RESULT OBJECT
        # ====================================================

        result_data = {

            "success":
                True,

            "image":
                (
                    "data:image/jpeg;base64,"
                    + image_base64
                ),

            "filename":
                file.filename,

            "detections":
                detections,

            "unique_damages":
                unique_damages,

            "damage_count":
                len(detections)

        }


        # ====================================================
        # DISPLAY RESULTS ON SAME PAGE
        # ====================================================

        return render_template(
            "index.html",
            result=result_data
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        print(
            f"Prediction error: {error}"
        )


        return render_template(
            "index.html",
            result={
                "success": False,
                "error":
                    (
                        "Unable to process the image. "
                        "Please try another vehicle image."
                    )
            }
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {
        "status":
            "healthy",

        "application":
            "Vehicle Damage Detection",

        "model":
            "YOLO26"
    }


# ============================================================
# APPLICATION ENTRY POINT
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