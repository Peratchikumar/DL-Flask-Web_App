# 🚗 Vehicle Damage Detection using YOLO26 + Flask

A professional Deep Learning web application for detecting **vehicle damage from images** using a custom-trained **YOLO26 object detection model** and a **Flask-based web application**.

The application allows users to upload a vehicle image and receive AI-powered vehicle damage detection results, including detected classes, confidence scores, and bounding-box coordinates.

---

## 🚀 Project Overview

Vehicle damage detection is a practical Computer Vision application that can help automate the identification and localization of damaged areas on vehicles.

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
- ☁️ Cloud Deployment

---

## ✨ Key Features

- 🚗 Vehicle damage detection
- 🧠 Custom-trained YOLO26 model
- 📷 Image upload
- 🎯 Bounding-box detection
- 📊 Confidence scores
- 🔢 Detection count
- 🔐 Secure file handling
- ⚡ YOLO26 inference
- 🌐 REST API
- 🎨 Modern responsive frontend
- 🩺 Health-check endpoint
- 📋 Application information endpoint
- 📦 Modular project architecture
- 🚀 Gunicorn production server
- ☁️ Deployment-ready Flask application

---

# 🧠 Deep Learning Workflow

```text
Vehicle Image
      │
      ▼
Image Upload
      │
      ▼
Flask Application
      │
      ▼
File Validation
      │
      ▼
Secure File Storage
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
├── app.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── models/
│   └── vehicle_damage_yolo26_best.pt
│
├── routes/
│   ├── __init__.py
│   └── prediction.py
│
├── services/
│   ├── __init__.py
│   └── detector.py
│
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   └── response_utils.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── uploads/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

---

# 📁 Folder and File Description

| File / Folder | Purpose |
|---|---|
| `app.py` | Main Flask application |
| `config/__init__.py` | Marks `config` as a Python package |
| `config/settings.py` | Application, model, upload, and inference configuration |
| `models/` | Stores the trained model |
| `vehicle_damage_yolo26_best.pt` | Single YOLO26 PyTorch model |
| `routes/__init__.py` | Marks `routes` as a Python package |
| `routes/prediction.py` | Prediction API endpoint |
| `services/__init__.py` | Marks `services` as a Python package |
| `services/detector.py` | Loads YOLO26 and performs inference |
| `utils/__init__.py` | Marks `utils` as a Python package |
| `utils/file_utils.py` | File validation and file-management utilities |
| `utils/response_utils.py` | API response utilities |
| `templates/index.html` | Main frontend interface |
| `static/css/style.css` | Frontend styling |
| `static/js/app.js` | Frontend API communication and interaction |
| `uploads/` | Runtime uploaded images |
| `outputs/` | Runtime generated output files |
| `.gitkeep` | Preserves empty runtime directories in Git |
| `.gitignore` | Prevents unnecessary and sensitive files from being committed |
| `requirements.txt` | Python dependencies |
| `Procfile` | Production Gunicorn start command |
| `README.md` | Project documentation |

---

# 🤖 Deep Learning Model

This application uses **one YOLO26 PyTorch model**:

```text
models/
└── vehicle_damage_yolo26_best.pt
```

### Model Details

```text
Architecture : YOLO26
Framework    : Ultralytics
Format       : PyTorch (.pt)
Task         : Object Detection
Model Count  : 1
```

The application directly loads the `.pt` model for inference.

### Model Path

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

```text
Input Image
     │
     ▼
Upload Validation
     │
     ▼
Secure Filename
     │
     ▼
Save to uploads/
     │
     ▼
YOLO26 Inference
     │
     ▼
Detection Results
     │
     ├── Class ID
     ├── Class Name
     ├── Confidence
     └── Bounding Box
     │
     ▼
JSON Response
     │
     ▼
Frontend
```

---

# ⚙️ Configuration

Application configuration is centralized in:

```text
config/settings.py
```

Important settings include:

```python
MODEL_PATH
IMAGE_SIZE
CONFIDENCE_THRESHOLD
IOU_THRESHOLD
UPLOAD_FOLDER
OUTPUT_FOLDER
MAX_CONTENT_LENGTH
APP_NAME
APP_VERSION
DEBUG
```

Example:

```python
MODEL_PATH = BASE_DIR / "models" / "vehicle_damage_yolo26_best.pt"

IMAGE_SIZE = 640

CONFIDENCE_THRESHOLD = 0.25

IOU_THRESHOLD = 0.45
```

---

# 📡 API Endpoints

## 🏠 Home

```text
GET /
```

Displays the main Vehicle Damage Detection interface.

---

## 🎯 Prediction

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
    "original_filename": "vehicle.jpg",
    "filename": "a1b2c3d4_vehicle.jpg",
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

> **Note:** The class name `"damage"` above is only an example. The actual class names are determined by the trained YOLO26 model.

---

## 🩺 Health Check

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

## ℹ️ Application Information

```text
GET /api/info
```

Returns basic application and model information.

Example:

```json
{
    "success": true,
    "application": "Vehicle Damage Detection",
    "version": "1.0.0",
    "model": "YOLO26",
    "model_format": "PyTorch (.pt)",
    "model_count": 1
}
```

---

# 💻 Technologies Used

## Programming Language

- Python

## Deep Learning

- YOLO26
- Ultralytics
- PyTorch

## Computer Vision

- OpenCV
- Pillow
- NumPy

## Backend

- Flask
- Werkzeug

## Frontend

- HTML5
- CSS3
- JavaScript

## Production Server

- Gunicorn

## Deployment

- Render

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

# ▶️ Run Locally

Start the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🔍 How to Use

1. Open the web application.
2. Select a vehicle image.
3. Upload the image.
4. Click the prediction/detection button.
5. The frontend sends the image to the Flask API.
6. The image is processed by YOLO26.
7. Detected objects are returned.
8. Confidence scores and bounding boxes are provided.
9. The frontend displays the prediction results.

---

# 🔐 File Handling

Uploaded files are stored temporarily in:

```text
uploads/
```

Generated prediction files can be stored in:

```text
outputs/
```

Only `.gitkeep` files are committed to GitHub for these runtime directories.

Actual uploaded images and generated prediction files should not be committed.

---

# 🚀 Deployment

This project is structured for production deployment using **Gunicorn**.

The `Procfile` contains:

```text
web: gunicorn app:app
```

### Render Configuration

Recommended build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```

The repository root should contain:

```text
app.py
requirements.txt
Procfile
```

---

# 🧪 Testing

## Start the application

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

# 🛡️ Security Considerations

The application includes:

- Secure uploaded filenames
- File-extension validation
- Maximum upload-size restriction
- Runtime upload/output directories
- `.env` protection through `.gitignore`
- Separation of application configuration
- Modular Flask architecture

Never commit secrets, API keys, passwords, or `.env` files to GitHub.

---

# 📈 Future Improvements

Potential improvements include:

- 🎥 Video-based vehicle damage detection
- 📱 Advanced mobile optimization
- 📊 Detection analytics dashboard
- 🧾 Automated damage reports
- 💰 Vehicle repair cost estimation
- 🗃️ Prediction history
- ☁️ Cloud storage integration
- 🔐 User authentication
- 🚘 Additional vehicle damage classes
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

💻 **GitHub**

https://github.com/Peratchikumar

📦 **Project Repository**

https://github.com/Peratchikumar/DL-Flask-Web_App

💼 **LinkedIn**

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