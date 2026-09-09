# Vehicle Damage Detector - Flask app

A small Flask app that wraps your trained YOLO26 vehicle-damage model in an
upload-a-photo web UI, built to deploy cleanly on Render.

## Why this doesn't use `ultralytics`/PyTorch

Render's Free and Starter web services both cap out at **512MB RAM**.
`ultralytics` pulls in PyTorch as a hard dependency, and torch + a loaded
model routinely uses several hundred MB by itself - too tight a fit
alongside the OS and Flask. This app instead runs your exported `.onnx`
model directly through **onnxruntime**, which needs a fraction of the RAM
and has no PyTorch dependency at all. Since your model was trained with
YOLO26's default "end-to-end" export, NMS is already baked into the ONNX
graph - `app.py` just has to run the session and filter by confidence, no
extra detection-decoding logic needed.

If you'd rather deploy with `ultralytics` directly (e.g. because you also
want the video-inference code from your notebook), that's simpler code but
means picking Render's **Standard** plan (2GB RAM, $25/mo) instead of
Free/Starter - see "Alternative" at the bottom.

## 1. Model file

Already done - `models/best.onnx` in this zip **is** your trained model,
exported from `vehicle_damage_yolo26_best.pt` at `imgsz=320` (matching how
it was trained). I loaded your checkpoint, confirmed its 14 class names
match what's hardcoded in `app.py`, exported it, and ran a real request
through the whole app locally before packaging this - nothing to do here.

If you retrain later and need to re-export:

```bash
pip install ultralytics
yolo export model=best.pt format=onnx imgsz=320
# creates best.onnx next to best.pt - copy it into models/, overwriting the old one
```

**If a future retrain changes your class list**, update `CLASS_NAMES` near
the top of `app.py` to match your `data.yaml` `names:` field exactly, in
the same order.

## 2. Run it locally first

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`, upload a photo, confirm you get boxes back
before touching Render at all - it's much faster to debug locally.

## 3. Push to GitHub

Render deploys from a git repo, so this needs to be in one:

```bash
git init
git add .
git commit -m "Vehicle damage detector"
git branch -M main
git remote add origin https://github.com/<you>/vehicle-damage-app.git
git push -u origin main
```

## 4. Deploy on Render

**Option A - Blueprint (uses the included `render.yaml`):**
1. In the Render dashboard: **New > Blueprint**.
2. Connect the GitHub repo you just pushed.
3. Render reads `render.yaml` and pre-fills everything - review and click
   **Apply**.

**Option B - manual setup:**
1. **New > Web Service**, connect your repo.
2. **Runtime:** Python 3
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `gunicorn app:app --workers 1 --threads 4 --timeout 120`
5. **Instance Type:** Starter ($7/mo, always-on) is the safe minimum given
   the RAM discussion above. Free will often work too for a demo/portfolio
   project - it just sleeps after inactivity and takes ~30-60s to wake back
   up on the next request.
6. Click **Create Web Service**.

Either way, the first build takes a few minutes (installing onnxruntime).
Once it's live, Render gives you a URL like
`https://vehicle-damage-detector.onrender.com`.

### Why `--workers 1`
Each gunicorn worker loads its own copy of the model into memory. On a
512MB instance, one worker with a few threads (to handle concurrent
requests without blocking) is the right shape - not more workers.

## 5. Sanity-check the deploy

- `GET /health` should return `{"status": "ok"}` - point any uptime
  monitor at this instead of `/`.
- Upload a real damage photo through the deployed URL and confirm the
  boxes and class names look right, exactly like you did locally.

## Notes / things worth knowing

- **Confidence threshold** is `CONF_THRESHOLD = 0.35` in `app.py`. Your
  notebook used `0.4` for images and `0.25` for video - tune this to
  taste once you see real traffic.
- **Free tier cold starts:** if you use the Free instance, the first
  request after ~15 minutes of inactivity will take 30-60s while the
  container wakes up. Starter ($7/mo) removes this by staying always-on.
- **Upload size** is capped at 8MB (`MAX_UPLOAD_MB` in `app.py`) so a
  stray huge photo can't blow up the process.
- This app only serves image uploads. Real-time video through a web
  request isn't a good fit for Render's CPU-only free/cheap tiers (long
  processing times risk request timeouts) - if you want the moving-video
  demo from your notebook online too, that's a separate piece of work
  (e.g. process short clips as a background job, or stream frame-by-frame
  over a websocket) rather than a single POST /predict call.

## Alternative: deploying with `ultralytics` instead

If you'd rather keep the exact `model.predict()` code from your notebook:

```python
from ultralytics import YOLO
model = YOLO("models/best.pt")
results = model.predict(image, conf=0.4)[0]
```

replace `onnxruntime`/`numpy`/`Pillow` pre/post-processing in `app.py`
with this, add `ultralytics` to `requirements.txt`, and use `best.pt`
instead of `best.onnx`. Simpler code, but you'll want Render's **Standard**
plan (2GB RAM) rather than Free/Starter to comfortably fit PyTorch +
Ultralytics in memory.
