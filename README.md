# 🚗 Vehicle Damage Detection using YOLO26 + Flask

A professional Deep Learning web application for detecting **vehicle damage from images** using a custom-trained **YOLO26 object detection model** and a **Flask-based web application**.

The application allows users to upload a vehicle image and receive AI-powered vehicle damage detection results with confidence scores and bounding-box information.

---

## 🚀 Project Overview

Vehicle damage detection is an important Computer Vision application that can help automate the identification and localization of damaged areas on vehicles.

This project combines:

- 🧠 Deep Learning
- 👁️ Computer Vision
- 🎯 YOLO26 Object Detection
- 🐍 Python
- 🌐 Flask
- 🎨 HTML5
- 🎨 CSS3
- ⚡ JavaScript
- 📡 REST API
- 🚀 Gunicorn

---

## ✨ Key Features

- 🚗 Vehicle damage detection
- 🧠 Custom-trained YOLO26 model
- 📷 Vehicle image upload
- 🎯 Bounding-box detection
- 📊 Confidence score
- 🔢 Detection count
- 🔐 Secure file handling
- ⚡ Fast model inference
- 🌐 Flask REST API
- 🎨 Modern responsive frontend
- 🩺 Health-check endpoint
- 📦 Modular project architecture
- 🚀 Deployment-ready structure

---

# 🧠 Deep Learning Workflow

```text
Vehicle Image
      │
      ▼
Image Upload
      │
      ▼
Flask API
      │
      ▼
File Validation
      │
      ▼
YOLO26 Detector
      │
      ▼
vehicle_damage_yolo26_best.pt
      │
      ▼
Object Detection
      │
      ├── Damage Class
      ├── Confidence Score
      └── Bounding Box
      │
      ▼
JSON Response
      │
      ▼
Frontend Visualization
```

---

# 🏗️ Project Structure

```text
DL-Flask-Web_App/
│
├── config/
│   └── settings.py
│
├── models/
│   └── vehicle_damage_yolo26_best.pt
│
├── routes/
│   └── prediction.py
│
├── services/
│   └── detector.py
│
├── utils/
│   ├── file_utils.py
│   └── response_utils.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── uploads/
│   └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
├── .gitignore
├── app.py
├── Procfile
├── README.md
└── requirements.txt
```

---

# 📁 File and Folder Description

| File / Folder | Description |
|---|---|
| `app.py` | Main Flask application |
| `config/settings.py` | Application and model configuration |
| `models/` | Contains the trained YOLO26 model |
| `vehicle_damage_yolo26_best.pt` | Trained YOLO26 PyTorch model |
| `routes/prediction.py` | Flask prediction API |
| `services/detector.py` | YOLO26 model loading and inference |
| `utils/file_utils.py` | File validation and file management |
| `utils/response_utils.py` | API response utilities |
| `templates/index.html` | Main web interface |
| `static/css/style.css` | Frontend styling |
| `static/js/app.js` | Frontend JavaScript |
| `uploads/` | Temporary uploaded images |
| `outputs/` | Generated output files |
| `.gitkeep` | Keeps empty directories tracked by Git |
| `.gitignore` | Prevents unnecessary files from being committed |
| `requirements.txt` | Python dependencies |
| `Procfile` | Production server configuration |
| `README.md` | Project documentation |

---

# 🤖 Deep Learning Model

This application uses **one trained YOLO26 PyTorch model**.

```text
models/
└── vehicle_damage_yolo26_best.pt
```

### Model Format

```text
Model: YOLO26
Framework: Ultralytics
Format: PyTorch (.pt)
Task: Object Detection
```

The application uses the `.pt` model directly for inference.

### Model Configuration

The model path is configured in:

```text
config/settings.py
```

Example:

```python
MODEL_PATH = BASE_DIR / "models" / "vehicle_damage_yolo26_best.pt"
```

---

# 🎯 Detection Pipeline

The application follows this pipeline:

```text
Input Image
    ↓
File Validation
    ↓
Secure Filename
    ↓
Temporary Upload
    ↓
YOLO26 Inference
    ↓
Detection Results
    ↓
Confidence Calculation
    ↓
Bounding Box Extraction
    ↓
JSON Response
    ↓
Frontend Display
```

---

# ⚙️ Configuration

Application configuration is centralized in:

```text
config/settings.py
```

Important configuration values include:

```python
MODEL_PATH
IMAGE_SIZE
CONFIDENCE_THRESHOLD
IOU_THRESHOLD
UPLOAD_FOLDER
OUTPUT_FOLDER
MAX_CONTENT_LENGTH
```

Example:

```python
MODEL_PATH = BASE_DIR / "models" / "vehicle_damage_yolo26_best.pt"

IMAGE_SIZE = 320

CONFIDENCE_THRESHOLD = 0.25

IOU_THRESHOLD = 0.45
```

---

# 📡 API Endpoints

## 1. Home

```text
GET /
```

Opens the main vehicle damage detection interface.

---

## 2. Prediction

```text
POST /api/predict
```

### Request

Upload an image using the form field:

```text
file
```

### cURL Example

```bash
curl -X POST \
  -F "file=@vehicle.jpg" \
  http://127.0.0.1:5000/api/predict
```

### Example Response

```json
{
    "success": true,
    "filename": "vehicle.jpg",
    "detection_count": 2,
    "detections": [
        {
            "class_id": 0,
            "class_name": "damage",
            "confidence": 0.9234,
            "confidence_percent": 92.34,
            "bounding_box": {
                "x1": 125.2,
                "y1": 84.6,
                "x2": 482.7,
                "y2": 361.4
            }
        }
    ]
}
```

---

## 3. Health Check

```text
GET /health
```

Example:

```text
http://127.0.0.1:5000/health
```

Example response:

```json
{
    "status": "healthy",
    "application": "Vehicle Damage Detection",
    "version": "1.0.0"
}
```

---

## 4. Application Information

```text
GET /api/info
```

Returns basic information about the application and the YOLO26 model.

---

# 💻 Technologies Used

### Programming

- Python

### Deep Learning

- YOLO26
- Ultralytics
- PyTorch

### Computer Vision

- OpenCV
- Pillow
- NumPy

### Backend

- Flask
- Werkzeug

### Frontend

- HTML5
- CSS3
- JavaScript

### Deployment

- Gunicorn

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Peratchikumar/DL-Flask-Web_App.git
```

---

## 2. Navigate to the Project

```bash
cd DL-Flask-Web_App
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🔍 How to Use

1. Open the web application.
2. Select a vehicle image.
3. Upload the image.
4. Click **Analyze Vehicle Damage**.
5. The frontend sends the image to the Flask API.
6. YOLO26 processes the image.
7. Detected damage classes are returned.
8. Confidence scores are displayed.
9. Bounding-box information is returned by the API.

---

# 🔐 File Handling

Uploaded images are stored temporarily in:

```text
uploads/
```

Generated files can be stored in:

```text
outputs/
```

The `.gitkeep` files ensure these directories remain available in Git even when they contain no files.

Uploaded filenames are sanitized using Werkzeug's secure filename utilities.

---

# 🚀 Production Deployment

The project includes a `Procfile` for deployment using Gunicorn.

```text
web: gunicorn app:app
```

The command starts the Flask application through Gunicorn.

---

# 📋 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

The project requires packages including:

```text
Flask
Werkzeug
Ultralytics
OpenCV
Pillow
NumPy
Gunicorn
```

---

# 🧪 Testing

## Run the application

```bash
python app.py
```

## Test health endpoint

```text
GET /health
```

## Test prediction endpoint

```text
POST /api/predict
```

## Test application information

```text
GET /api/info
```

---

# 📈 Future Improvements

Possible future enhancements include:

- 🎥 Video vehicle damage detection
- 📱 Improved mobile interface
- 📊 Analytics dashboard
- 🧾 Automated damage reports
- 💰 Repair cost estimation
- 🗃️ Prediction history
- ☁️ Cloud storage
- 🔐 User authentication
- 🚘 Additional damage categories
- ⚡ GPU inference
- 🐳 Docker deployment
- 📈 Model performance monitoring

---

# 👨‍💻 Author

## Peratchi Kumar K

**Machine Learning | Deep Learning | Computer Vision | Python | Flask**

### GitHub

https://github.com/Peratchikumar

### Project Repository

https://github.com/Peratchikumar/DL-Flask-Web_App

### LinkedIn

https://www.linkedin.com/in/peratchi-kumar-k-167076289/

---

# 🌐 Connect With Me

💻 GitHub:

https://github.com/Peratchikumar

📦 Project:

https://github.com/Peratchikumar/DL-Flask-Web_App

💼 LinkedIn:

https://www.linkedin.com/in/peratchi-kumar-k-167076289/

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

# 📜 License

This project is intended for educational, portfolio, and demonstration purposes.

---

# 🚗 Vehicle Damage Detection

**YOLO26 + Python + Flask**

> Turning Computer Vision into a practical AI-powered application.