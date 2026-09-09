"""
Vehicle Damage Detection - Flask app
-------------------------------------
Serves a single-page upload form, runs the trained YOLO26 model (exported
to ONNX) on the uploaded image using onnxruntime, and returns the image
with damage boxes drawn on it plus a list of detections.

Deliberately built on onnxruntime instead of the `ultralytics` package so
the whole app (Flask + onnxruntime + numpy + Pillow) stays well under
~200MB of RAM at runtime - this fits Render's free/Starter (512MB) tier.
`ultralytics` would also work, but it pulls in PyTorch as a hard
dependency, which is heavier than most free/cheap hosting tiers can hold
alongside the OS + Flask + your other services.

YOLO26's default ONNX export is "end-to-end": NMS is already baked into
the graph, so the output is (1, 300, 6) = up to 300 boxes formatted as
[x1, y1, x2, y2, confidence, class_id] in the *input* pixel space. No
extra NMS step is needed here - just a confidence filter and undoing the
letterbox resize to map boxes back to the original image.
"""

import base64
import io
import os
import time

import numpy as np
import onnxruntime as ort
from flask import Flask, render_template, request
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.onnx")

IMG_SIZE = 320          # must match the imgsz the model was trained/exported with
CONF_THRESHOLD = 0.1   # raise this if you're getting too many false positives
MAX_UPLOAD_MB = 8

# Same order as data_config["names"] in the training notebook's data.yaml
CLASS_NAMES = [
    "Front-windscreen-damage", "Headlight-damage", "Rear-windscreen-Damage",
    "Runningboard-Damage", "Sidemirror-Damage", "Taillight-Damage",
    "bonnet-dent", "boot-dent", "doorouter-dent", "fender-dent",
    "front-bumper-dent", "quaterpanel-dent", "rear-bumper-dent", "roof-dent",
]

BOX_COLORS = [
    (230, 25, 75), (60, 180, 75), (255, 196, 25), (0, 130, 200),
    (245, 130, 48), (145, 30, 180), (70, 200, 200), (240, 50, 190),
    (190, 215, 40), (250, 150, 170), (0, 128, 128), (180, 150, 255),
    (170, 110, 40), (210, 70, 70),
]

# ---------------------------------------------------------------------------
# App + model setup (loaded once per process, not per-request)
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

_session = None
_input_name = None


def get_session():
    """Lazy-load the ONNX model on first request so the app boots even if
    the model file isn't in place yet (you'll just get a clear error)."""
    global _session, _input_name
    if _session is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Copy your trained "
                f"best.onnx into the models/ folder before running the app."
            )
        _session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
        _input_name = _session.get_inputs()[0].name
    return _session, _input_name


# ---------------------------------------------------------------------------
# Pre/post-processing
# ---------------------------------------------------------------------------
def letterbox(image, new_size=IMG_SIZE):
    """Resize with unchanged aspect ratio using grey padding, matching the
    preprocessing Ultralytics uses internally during training/export."""
    w, h = image.size
    scale = min(new_size / w, new_size / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = image.resize((nw, nh), Image.BILINEAR)

    canvas = Image.new("RGB", (new_size, new_size), (114, 114, 114))
    pad_x, pad_y = (new_size - nw) // 2, (new_size - nh) // 2
    canvas.paste(resized, (pad_x, pad_y))
    return canvas, scale, pad_x, pad_y


def preprocess(image):
    letterboxed, scale, pad_x, pad_y = letterbox(image)
    arr = np.asarray(letterboxed, dtype=np.float32) / 255.0
    arr = arr.transpose(2, 0, 1)          # HWC -> CHW
    arr = np.expand_dims(arr, axis=0)     # add batch dim -> NCHW
    return arr, scale, pad_x, pad_y


def postprocess(detections, scale, pad_x, pad_y, orig_w, orig_h):
    # `detections` is already the (300, 6) array for a single image:
    # x1, y1, x2, y2, confidence, class_id - batch dim was dropped by the caller.
    results = []
    for x1, y1, x2, y2, conf, cls_id in detections:
        if conf < CONF_THRESHOLD:
            continue
        x1 = (x1 - pad_x) / scale
        y1 = (y1 - pad_y) / scale
        x2 = (x2 - pad_x) / scale
        y2 = (y2 - pad_y) / scale
        x1, x2 = float(np.clip(x1, 0, orig_w)), float(np.clip(x2, 0, orig_w))
        y1, y2 = float(np.clip(y1, 0, orig_h)), float(np.clip(y2, 0, orig_h))
        cls_id = int(cls_id)
        color = BOX_COLORS[cls_id % len(BOX_COLORS)]
        results.append({
            "box": [x1, y1, x2, y2],
            "confidence": float(conf),
            "class_id": cls_id,
            "class_name": CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else f"class_{cls_id}",
            "color_hex": "#%02x%02x%02x" % color,
        })
    results.sort(key=lambda d: d["confidence"], reverse=True)
    return results


def draw_detections(image, detections):
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        color = BOX_COLORS[det["class_id"] % len(BOX_COLORS)]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        label = f'{det["class_name"]} {det["confidence"]:.2f}'
        text_box = draw.textbbox((x1, y1), label)
        draw.rectangle(
            [text_box[0], text_box[1] - 4, text_box[2] + 4, text_box[3] + 2],
            fill=color,
        )
        draw.text((x1 + 2, y1 - 2), label, fill=(15, 15, 15))
    return annotated


def image_to_base64(image):
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return render_template("index.html", error="Choose an image first.")

    try:
        image = Image.open(file.stream).convert("RGB")
    except Exception:
        return render_template("index.html", error="That file doesn't look like a valid image.")

    try:
        session, input_name = get_session()
    except FileNotFoundError as exc:
        return render_template("index.html", error=str(exc))

    orig_w, orig_h = image.size
    tensor, scale, pad_x, pad_y = preprocess(image)

    start = time.time()
    raw_output = session.run(None, {input_name: tensor})[0][0]  # drop batch dim
    infer_ms = round((time.time() - start) * 1000, 1)

    detections = postprocess(raw_output, scale, pad_x, pad_y, orig_w, orig_h)
    annotated = draw_detections(image, detections)

    return render_template(
        "index.html",
        result_image=image_to_base64(annotated),
        detections=detections,
        infer_ms=infer_ms,
    )


@app.route("/health")
def health():
    """Simple endpoint for Render's health checks / uptime pings."""
    return {"status": "ok"}


if __name__ == "__main__":
    # Local dev only - Render runs this via gunicorn (see Procfile/render.yaml)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
