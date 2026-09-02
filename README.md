# 🚗 DriveInspect — AI Vehicle Damage Detection

AI-powered vehicle damage detection web application built using YOLO26, Flask, Python, HTML5, CSS3, and JavaScript.

DriveInspect allows users to upload a vehicle image and automatically detect visible vehicle damage using a trained YOLO26 object detection model. The application displays the processed image with bounding boxes along with detection statistics and confidence information.

---

## ✨ Features

- 🚗 AI-powered vehicle damage detection
- 🧠 YOLO26 object detection
- 🖼️ Image-only input
- 📤 Drag-and-drop image upload
- 👁️ Image preview before analysis
- 🎯 Bounding-box detection
- 📊 Total detection count
- 📈 Average confidence score
- 📋 Damage class distribution
- 🔎 Individual detection confidence
- ⚡ Flask backend
- 🎨 Premium responsive frontend
- 📱 Desktop and mobile responsive design
- 🔒 Local YOLO26 inference
- 🐍 Python-based machine learning backend

---

## 🛠️ Technology Stack

### Machine Learning
- YOLO26
- Ultralytics
- PyTorch
- OpenCV
- Pillow

### Backend
- Python
- Flask
- Werkzeug

### Frontend
- HTML5
- CSS3
- JavaScript
- Google Fonts

---

## 📁 Project Structure

vehicle_damage_detection/
│
├── app.py
├── vehicle_damage_yolo26_best.pt
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│   └── .gitkeep
│
└── results/
    └── .gitkeep

---

## 🧠 Model

DriveInspect uses a trained YOLO26 Nano object detection model.

Model file:

vehicle_damage_yolo26_best.pt

The model is loaded by the Flask backend and used to detect vehicle damage from uploaded images.

---

## 🎯 Vehicle Damage Classes

The trained model contains 14 vehicle damage classes:

1. Front-windscreen-damage
2. Headlight-damage
3. Rear-windscreen-Damage
4. Runningboard-Damage
5. Sidemirror-Damage
6. Taillight-Damage
7. bonnet-dent
8. boot-dent
9. doorouter-dent
10. fender-dent
11. front-bumper-dent
12. quaterpanel-dent
13. rear-bumper-dent
14. roof-dent

---

## 📊 Model Performance

The trained model achieved the following validation results:

| Metric | Score |
|---|---:|
| Precision | 0.657 |
| Recall | 0.567 |
| mAP@50 | 0.627 |
| mAP@50-95 | 0.386 |

These metrics represent the validation performance of the trained model.

---

## 🧪 Training Configuration

| Parameter | Value |
|---|---:|
| Model | YOLO26 Nano |
| Epochs | 20 |
| Image Size | 320 |
| Batch Size | 8 |
| Patience | 5 |
| Project | damage_detection |
| Run Name | yolo26_run1 |

---

## ⚙️ Detection Configuration

The application performs YOLO26 inference using the trained model.

Detection settings:

- Confidence threshold: 0.25
- Image size: 320
- Model: YOLO26 Nano
- Input type: Image
- Maximum upload size: 100 MB

---

## 🖼️ Supported Image Formats

DriveInspect accepts:

- JPG
- JPEG
- PNG
- WEBP
- BMP

Maximum upload size:

100 MB

Video input is not supported by the current application.

---

## 🚀 Installation

### 1. Download or Clone the Project

Download the project and extract it to your computer.

Or clone the repository:

git clone YOUR_REPOSITORY_URL

---

### 2. Open the Project Folder

cd vehicle_damage_detection

---

### 3. Create a Virtual Environment

#### Windows

python -m venv venv

Activate it:

venv\Scripts\activate

#### macOS / Linux

python3 -m venv venv

Activate it:

source venv/bin/activate

---

### 4. Install Dependencies

pip install -r requirements.txt

---

### 5. Verify the Model

Make sure the trained YOLO26 model exists in the project root:

vehicle_damage_detection/
│
├── app.py
└── vehicle_damage_yolo26_best.pt

The model filename must be:

vehicle_damage_yolo26_best.pt

---

## ▶️ Run the Application

Start the Flask server:

python app.py

The application should run at:

http://127.0.0.1:5000

Open that address in your web browser.

---

## ⚠️ Important: Do Not Open index.html Directly

Do not open:

templates/index.html

directly in Chrome.

Do not use Live Server for this Flask application.

Instead, start the Flask backend:

python app.py

Then open:

http://127.0.0.1:5000

Flask renders:

templates/index.html

and automatically serves:

static/style.css
static/script.js

---

## 🔗 Frontend File Linking

The HTML file should load the CSS using Flask's static URL:

<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

The JavaScript should be loaded using:

<script src="{{ url_for('static', filename='script.js') }}"></script>

The files must be located exactly here:

templates/
└── index.html

static/
├── style.css
└── script.js

---

## 🖥️ How to Use DriveInspect

### Step 1 — Open the Application

Open:

http://127.0.0.1:5000

### Step 2 — Upload Vehicle Image

You can:

- Drag and drop an image
- Click the upload area
- Choose an image from your device

Supported formats:

JPG
JPEG
PNG
WEBP
BMP

### Step 3 — Preview

After selecting an image, the application displays an image preview.

The selected filename and file size are also displayed.

### Step 4 — Analyze

Click:

Analyze Vehicle

The frontend sends the selected image to:

POST /predict

### Step 5 — YOLO26 Processing

The Flask backend receives the image and passes it to the trained YOLO26 model.

The model analyzes the image and identifies visible vehicle damage.

### Step 6 — View Results

After processing, DriveInspect displays:

- Detection result image
- Bounding boxes
- Total detections
- Average confidence
- Number of damage types
- Damage class distribution
- Individual detection confidence

---

## 🔄 Application Workflow

USER
  ↓
Upload Vehicle Image
  ↓
Frontend Validation
  ↓
POST /predict
  ↓
Flask Backend
  ↓
YOLO26 Model
  ↓
Vehicle Damage Detection
  ↓
Annotated Image
  ↓
JSON Response
  ↓
DriveInspect UI
  ↓
Detection Results

---

## 🔌 API

The application provides the following prediction endpoint:

POST /predict

The uploaded image is submitted using the form field:

file

The frontend sends the image to the Flask backend, where the YOLO26 model performs inference.

---

## 📤 API Response

A successful prediction returns JSON containing information such as:

{
    "success": true,
    "message": "Vehicle damage detection completed successfully.",
    "filename": "vehicle.jpg",
    "media_type": "image",
    "result_url": "/results/example/result.jpg",
    "total_detections": 2,
    "average_confidence": 84.5,
    "damage_counts": {
        "bonnet-dent": 1,
        "headlight-damage": 1
    },
    "detections": [
        {
            "class": "bonnet-dent",
            "confidence": 88.2
        },
        {
            "class": "headlight-damage",
            "confidence": 80.8
        }
    ]
}

---

## 📂 Input and Output

### Input

Vehicle images in:

- JPG
- JPEG
- PNG
- WEBP
- BMP

### Output

The YOLO26 model generates an annotated image containing detected damage and bounding boxes.

Uploaded images are stored in:

uploads/

Generated detection results are stored in:

results/

---

## 🗂️ Important Files

### app.py

The Flask backend.

Responsibilities:

- Start the web application
- Load YOLO26
- Receive uploaded images
- Validate files
- Run model inference
- Save detection results
- Return JSON results
- Serve processed images

### vehicle_damage_yolo26_best.pt

The trained YOLO26 model.

This is the primary machine learning model used for vehicle damage detection.

### templates/index.html

The main web interface.

Responsibilities:

- Application layout
- Upload interface
- Image preview
- Processing interface
- Detection results
- Metrics
- Damage class display

### static/style.css

The visual design of DriveInspect.

Responsibilities:

- Premium dark interface
- Automotive visual style
- Responsive design
- Upload card
- Buttons
- Cards
- Animations
- Results dashboard
- Mobile layout

### static/script.js

Frontend application logic.

Responsibilities:

- File selection
- Drag and drop
- Image preview
- File validation
- Upload request
- Processing progress
- Error handling
- Detection result rendering
- Confidence visualization
- New inspection functionality

### requirements.txt

Contains the Python dependencies required to run the application.

Install them with:

pip install -r requirements.txt

---

## 🔐 File Validation

The application validates:

### File Extension

Allowed:

.jpg
.jpeg
.png
.webp
.bmp

### File Size

Maximum:

100 MB

### Empty Files

Empty uploads are rejected.

### Secure Filenames

Uploaded filenames are sanitized before saving.

---

## 📈 Detection Metrics

The application provides three primary dashboard metrics.

### Total Detections

The total number of detected damage objects.

Example:

3

### Average Confidence

The average confidence score across all detected objects.

Example:

86.4%

### Damage Types

The number of unique damage classes detected.

Example:

2

For example, if the model detects:

bonnet-dent
bonnet-dent
headlight-damage

Then:

Total detections = 3
Damage types = 2

---

## 🧩 Detection Example

A vehicle image could produce results such as:

bonnet-dent
headlight-damage

with confidence values such as:

bonnet-dent        91.2%
headlight-damage   83.7%

---

## 🐛 Troubleshooting

### CSS Is Not Loading

Verify:

vehicle_damage_detection/
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

Make sure index.html contains:

<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

Then restart Flask:

python app.py

Open:

http://127.0.0.1:5000

---

### JavaScript Is Not Working

Verify:

static/script.js

exists.

Make sure index.html contains:

<script src="{{ url_for('static', filename='script.js') }}"></script>

Then refresh the browser.

---

### Model Not Found

If you receive a model-not-found error, verify that:

vehicle_damage_yolo26_best.pt

is located in the same directory as:

app.py

Correct structure:

vehicle_damage_detection/
│
├── app.py
└── vehicle_damage_yolo26_best.pt

---

### Detection Fails

Check:

1. Flask is running.
2. The YOLO26 model exists.
3. The uploaded file is a supported image.
4. The image is less than 100 MB.
5. All requirements are installed.

Run:

pip install -r requirements.txt

Then restart:

python app.py

---

### Port 5000 Is Already in Use

Stop the existing Flask/Python process and restart the application.

Alternatively, configure the application port using the PORT environment variable.

---

## 🌐 Deployment

The application can be deployed to a suitable Python/Flask hosting platform.

Before production deployment, consider:

- Disable Flask debug mode
- Configure production environment variables
- Use a production WSGI server
- Configure persistent storage for uploaded images
- Configure appropriate upload limits
- Secure uploaded files
- Add authentication if required
- Configure logging
- Remove old uploaded results periodically

---

## 🚀 Future Improvements

Possible future improvements include:

- Vehicle damage severity classification
- Damage percentage estimation
- Damage-area measurement
- Automatic repair cost estimation
- PDF inspection reports
- Inspection history
- Database integration
- User authentication
- Cloud storage
- Advanced analytics dashboard
- Model retraining
- Additional vehicle damage classes
- Confidence threshold controls
- Multi-image inspection
- Insurance claim assistance
- Automated inspection summaries

---

## 🎓 Project Purpose

This project demonstrates an end-to-end computer vision application connecting:

Machine Learning
+
Object Detection
+
Python
+
Flask
+
HTML
+
CSS
+
JavaScript

The project can be used as:

- Machine Learning portfolio project
- Computer Vision project
- Flask deployment project
- YOLO object detection demonstration
- Academic project
- Interview project
- GitHub portfolio project

---

## 🏆 Project Highlights

Project Name:
DriveInspect

Domain:
Computer Vision / Machine Learning

Task:
Vehicle Damage Detection

Model:
YOLO26 Nano

Framework:
Ultralytics

Backend:
Flask

Frontend:
HTML5 + CSS3 + JavaScript

Input:
Vehicle Image

Output:
Annotated Vehicle Image + Detection Analytics

Damage Classes:
14

Maximum Upload Size:
100 MB

---

## 📌 Quick Start

Run the following commands:

git clone YOUR_REPOSITORY_URL

cd vehicle_damage_detection

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python app.py

Then open:

http://127.0.0.1:5000

---

## 📝 Project Notes

The trained YOLO26 model and its performance metrics are based on the project's training workflow.

The application is designed for visible vehicle damage detection from images.

Detection results depend on:

- Image quality
- Vehicle visibility
- Lighting conditions
- Camera angle
- Damage visibility
- Model training quality
- Detection confidence threshold

The system should therefore be considered an AI-assisted visual inspection tool rather than a replacement for professional physical vehicle inspection.

---

# 🚗 DriveInspect

## AI Vehicle Damage Detection

Built with:

🐍 Python
🌐 Flask
🧠 YOLO26
⚡ Ultralytics
🎨 HTML5
🎨 CSS3
⚙️ JavaScript

---

## ⭐ License

This project is intended for educational, portfolio, demonstration, and research purposes.