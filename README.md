# 🚗 Vehicle Damage Detection Using YOLO26

A deep learning-based **Vehicle Damage Detection System** built using **YOLO26, Python, Flask, OpenCV, and Computer Vision**.

This project uses a custom-trained **YOLO26n object detection model** to automatically detect and localize different types of vehicle damage from images.

The trained model is integrated into a **Flask web application**, allowing users to upload a vehicle image and receive an annotated result showing detected damage, bounding boxes, and confidence scores.

---

## 📌 Project Name

```text
DL_Vehicle_Damage_Detection
```

---

## 🎯 Project Objective

The objective of this project is to develop an automated vehicle damage detection system using deep learning and computer vision.

The application can:

- Upload a vehicle image
- Detect visible vehicle damage
- Identify the type of damage
- Locate damage using bounding boxes
- Calculate detection confidence
- Generate an annotated output image
- Display the prediction through a web interface

---

## 🧠 Project Overview

Manual vehicle damage inspection can be time-consuming and dependent on human expertise.

This project applies **Computer Vision and Object Detection** to automate the initial identification of visible vehicle damage.

The system uses a custom-trained **YOLO26n** model to detect different vehicle damage categories.

The trained model is connected to a Flask-based web application.

### Overall Workflow

```text
Vehicle Image
      ↓
Image Upload
      ↓
Flask Application
      ↓
YOLO26 Model
      ↓
Object Detection
      ↓
Damage Classification
      ↓
Bounding Boxes
      ↓
Confidence Scores
      ↓
Annotated Output
      ↓
Result Page
```

---

# ✨ Key Features

- 🚗 Vehicle damage detection
- 🤖 YOLO26 object detection
- 🧠 Custom-trained deep learning model
- 📷 Vehicle image upload
- 🎯 Bounding-box localization
- 📊 Confidence score calculation
- 🌐 Flask web application
- 🎨 Custom HTML/CSS interface
- ⚡ OpenCV image processing
- 📁 Automatic output generation
- 🚀 Gunicorn production server support
- ☁️ Cloud deployment ready

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLO26 | Object detection |
| Ultralytics | YOLO framework |
| PyTorch | Deep learning |
| OpenCV | Image processing |
| Flask | Web application |
| HTML5 | Frontend |
| CSS3 | Styling |
| JavaScript | Frontend interaction |
| Gunicorn | Production server |
| Git | Version control |
| GitHub | Repository hosting |
| Render | Cloud deployment |

---

# 🤖 Machine Learning Model

This project uses a custom-trained:

```text
YOLO26n
```

The trained deployment model is:

```text
vehicle_damage_yolo26_best.pt
```

Model location:

```text
model/vehicle_damage_yolo26_best.pt
```

The model is loaded by Flask during application startup.

---

# 📊 Model Configuration

```text
Model              : YOLO26n
Task               : Object Detection
Input Image Size   : 320 × 320
Confidence         : 0.40
Training Epochs    : 20
Model Format       : PyTorch (.pt)
Inference          : Image
```

The training workflow documented for this project used **20 epochs**, with the best model saved as `best.pt`. :contentReference[oaicite:0]{index=0}

The deployment artifact was named:

```text
vehicle_damage_yolo26_best.pt
```

:contentReference[oaicite:1]{index=1}

---

# 🎯 Vehicle Damage Classes

The model is trained to detect the following vehicle damage categories:

```text
1.  Front-windscreen-damage
2.  Headlight-damage
3.  Rear-windscreen-Damage
4.  Runningboard-Damage
5.  Sidemirror-Damage
6.  Taillight-Damage
7.  bonnet-dent
8.  boot-dent
9.  doorouter-dent
10. fender-dent
11. front-bumper-dent
12. quaterpanel-dent
13. rear-bumper-dent
14. roof-dent
```

---

# 📈 Model Evaluation

The documented validation results for the trained model were approximately:

| Metric | Score |
|---|---:|
| Precision | 0.657 |
| Recall | 0.567 |
| mAP@50 | 0.627 |
| mAP@50-95 | 0.386 |

These are the validation results recorded during the model training workflow. :contentReference[oaicite:2]{index=2}

---

# 🏗️ Project Architecture

```text
                     ┌───────────────────┐
                     │      User         │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   Web Browser     │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │ Flask Application │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │  Image Upload     │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │     YOLO26n       │
                     │   Detection Model │
                     └─────────┬─────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          Damage Class   Bounding Box   Confidence
                │              │              │
                └──────────────┼──────────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │ Annotated Image   │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   Result Page     │
                     └───────────────────┘
```

---

# 📂 Project Structure

```text
DL_Vehicle_Damage_Detection/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
│
├── model/
│   └── vehicle_damage_yolo26_best.pt
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│       └── logo.png
│
├── uploads/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

---

# 📁 Directory Description

## `app.py`

Main Flask application.

Responsible for:

- Loading the trained YOLO26 model
- Receiving uploaded images
- Running inference
- Extracting detected classes
- Extracting confidence scores
- Generating annotated images
- Returning prediction results

---

## `model/`

Contains the trained YOLO26 model.

```text
model/
└── vehicle_damage_yolo26_best.pt
```

---

## `templates/`

Contains Flask HTML templates.

```text
templates/
├── index.html
└── result.html
```

### `index.html`

Provides the image-upload interface.

### `result.html`

Displays the detection results.

---

## `static/`

Contains frontend assets.

```text
static/
├── css/
├── js/
└── images/
```

### CSS

```text
static/css/style.css
```

Contains application styling.

### JavaScript

```text
static/js/script.js
```

Contains frontend interaction.

### Logo

```text
static/images/logo.png
```

Contains the application logo.

---

## `uploads/`

Stores uploaded vehicle images.

```text
uploads/
└── .gitkeep
```

---

## `outputs/`

Stores processed images generated by the YOLO detection pipeline.

```text
outputs/
└── .gitkeep
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project:

```bash
cd DL_Vehicle_Damage_Detection
```

---

# 2. Create a Virtual Environment

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

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

The project requires:

```text
Flask
Werkzeug
Ultralytics
OpenCV
NumPy
Pillow
Gunicorn
```

The exact versions are specified in:

```text
requirements.txt
```

---

# 🤖 Model Setup

Make sure the trained model is placed at:

```text
model/vehicle_damage_yolo26_best.pt
```

The expected path is:

```text
DL_Vehicle_Damage_Detection/
└── model/
    └── vehicle_damage_yolo26_best.pt
```

The Flask application should load it using:

```python
MODEL_PATH = BASE_DIR / "model" / "vehicle_damage_yolo26_best.pt"
```

---

# ▶️ Run the Application Locally

Start the Flask application:

```bash
python app.py
```

The application will run on:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🌐 How to Use

## Step 1

Open:

```text
http://127.0.0.1:5000
```

---

## Step 2

Upload a vehicle image.

Supported formats:

```text
JPG
JPEG
PNG
WEBP
BMP
```

---

## Step 3

Click the detection/prediction button.

---

## Step 4

The YOLO26 model analyzes the image.

---

## Step 5

The application displays:

```text
Detected Damage
↓
Damage Class
↓
Confidence Score
↓
Bounding Box
↓
Annotated Image
```

---

# 🔍 Detection Process

The application uses the YOLO prediction process:

```python
results = model.predict(
    source=image_path,
    conf=0.40,
    imgsz=320,
    save=False
)
```

The model detects objects and returns:

- Class ID
- Class name
- Confidence score
- Bounding box coordinates

---

# 📷 Example

### Input

```text
Vehicle image containing visible damage
```

### Model Processing

```text
Input Image
     ↓
YOLO26n
     ↓
Object Detection
     ↓
Damage Localization
     ↓
Confidence Calculation
```

### Output

```text
Damage: front-bumper-dent
Confidence: 91.25%

Damage: headlight-damage
Confidence: 87.64%
```

The output image contains bounding boxes around the detected damage.

---

# 🧪 Testing

For testing, use images containing visible automobile damage.

Examples:

```text
✓ Damaged bumper
✓ Damaged bonnet
✓ Damaged door
✓ Damaged fender
✓ Damaged windshield
✓ Damaged headlight
✓ Damaged taillight
✓ Damaged side mirror
✓ Damaged roof
```

For better detection performance:

- Use clear images.
- Ensure the vehicle is visible.
- Avoid excessive blur.
- Use sufficient lighting.
- Keep the damaged region visible.
- Avoid extreme camera angles when possible.

---

# 🚀 Deployment

This project is structured for production deployment using:

```text
Flask + Gunicorn
```

The project contains:

```text
Procfile
```

with:

```text
web: gunicorn app:app
```

---

# ☁️ Render Deployment

## Step 1 — Push to GitHub

Push the complete project:

```text
DL_Vehicle_Damage_Detection/
```

to GitHub.

Make sure the repository contains:

```text
app.py
requirements.txt
Procfile
README.md
model/
templates/
static/
uploads/
outputs/
```

---

## Step 2 — Create Render Web Service

Create a new Web Service and connect your GitHub repository.

---

## Step 3 — Build Command

Use:

```bash
pip install -r requirements.txt
```

---

## Step 4 — Start Command

Use:

```bash
gunicorn app:app
```

---

## Step 5 — Deploy

Deploy the application.

The deployment process will:

```text
Install dependencies
       ↓
Start Flask application
       ↓
Load YOLO26 model
       ↓
Start Gunicorn
       ↓
Serve web application
```

---

# ⚠️ Important Deployment Requirement

The model file must be available at:

```text
model/vehicle_damage_yolo26_best.pt
```

If the model is missing, the application cannot perform predictions.

---

# 🔐 Security

For production use, additional security measures should be considered:

- Secure file validation
- MIME-type validation
- File-size restrictions
- Secure filenames
- Uploaded-file cleanup
- Rate limiting
- Authentication
- HTTPS
- Logging
- Resource management

The application should never blindly trust uploaded files.

---

# ⚠️ Limitations

This system is designed to detect **visible vehicle damage** based on the classes represented in its training dataset.

Detection performance can vary depending on:

- Image quality
- Lighting
- Camera angle
- Vehicle model
- Damage severity
- Background
- Occlusion
- Damage visibility
- Similarity to the training data

The system should be considered an **AI-assisted vehicle damage detection tool** and not a replacement for professional inspection.

---

# 🔮 Future Improvements

Future versions could include:

- 🎥 Video damage detection
- 📹 Real-time webcam detection
- 📱 Mobile-responsive application
- 📊 Damage severity estimation
- 💰 Repair-cost estimation
- 📄 Automated inspection reports
- 🧾 Insurance claim assistance
- 🗃️ Prediction history
- 🔐 User authentication
- ☁️ Cloud database integration
- 📈 Analytics dashboard
- ⚡ GPU inference
- 🔄 Model version management
- 🎯 Improved training dataset
- 🧠 Model accuracy improvements

---

# 🧩 Machine Learning Pipeline

```text
Dataset
   ↓
Data Preparation
   ↓
YOLO Dataset
   ↓
YOLO26n
   ↓
Model Training
   ↓
Validation
   ↓
Best Model
   ↓
vehicle_damage_yolo26_best.pt
   ↓
Flask Integration
   ↓
Web Application
   ↓
Vehicle Damage Detection
```

---

# 💡 Project Highlights

```text
Project Name     : DL_Vehicle_Damage_Detection
Project Type     : Deep Learning / Computer Vision
Application      : Vehicle Damage Detection
Model            : YOLO26n
Task             : Object Detection
Framework        : Ultralytics
Backend          : Flask
Frontend         : HTML / CSS / JavaScript
Image Processing : OpenCV
Model Format     : PyTorch (.pt)
Input Size       : 320 × 320
Confidence       : 0.40
Training         : 20 Epochs
Deployment       : Flask + Gunicorn
```

---

# 🎓 Skills Demonstrated

This project demonstrates practical knowledge of:

```text
Python
Machine Learning
Deep Learning
Computer Vision
Object Detection
YOLO
YOLO26
Ultralytics
PyTorch
OpenCV
Flask
HTML
CSS
JavaScript
Model Deployment
Git
GitHub
Cloud Deployment
```

---

# 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

- Understanding object detection
- Training a custom YOLO model
- Evaluating an object detection model
- Loading trained model weights
- Running inference on images
- Extracting detection results
- Drawing bounding boxes
- Building a Flask ML application
- Connecting a machine learning model to a web interface
- Structuring a deployable ML project
- Preparing a project for cloud deployment

---

# 🏆 Project Goal

The ultimate goal of this project is to demonstrate how a trained deep learning model can be transformed into a practical web-based application.

```text
Machine Learning Model
        +
Flask Application
        +
Frontend Interface
        +
Cloud Deployment
        ↓
Practical AI Application
```

---

# 👨‍💻 Author

## Peratchi Kumar

**Machine Learning | Deep Learning | Computer Vision | Python**

---

# ⭐ Acknowledgements

This project uses the **Ultralytics YOLO framework** for object detection and inference.

---

# 📄 License

This project is intended for:

- Educational purposes
- Learning
- Portfolio demonstration
- Machine learning experimentation

Before using the project commercially, verify the licenses and usage restrictions associated with the dataset, model, libraries, and other third-party components.

---

# ⭐ GitHub Repository

If you find this project useful, consider giving the repository a ⭐.

```text
DL_Vehicle_Damage_Detection
```

---

# 🚗 Vehicle Damage Detection

```text
UPLOAD
   ↓
DETECT
   ↓
LOCALIZE
   ↓
CLASSIFY
   ↓
DISPLAY
```

### Built with

```text
🐍 Python
🤖 YOLO26
🧠 Deep Learning
👁️ Computer Vision
🌐 Flask
⚡ OpenCV
🚀 Gunicorn
```

**Vehicle Damage Detection — Automated Computer Vision with YOLO26**