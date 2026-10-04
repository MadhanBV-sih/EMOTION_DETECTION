# 😊 Emotion Analyzer

A **real-time facial emotion detection** web application that uses your webcam to analyze your facial expressions and tell you what emotion you're showing — happy, sad, angry, surprised, fearful, disgusted, or neutral.

Built with **Python (Flask)** on the backend and **HTML/JavaScript** on the frontend, powered by **AI/Deep Learning** models for face detection and emotion recognition.

---

## 📖 Table of Contents

- [What Does This Project Do?](#-what-does-this-project-do)
- [How It Works (The Big Picture)](#-how-it-works-the-big-picture)
- [Technologies Used](#-technologies-used)
- [Project Structure (File Map)](#-project-structure-file-map)
- [Understanding Each File](#-understanding-each-file)
  - [run.py — The Starting Point](#1-runpy--the-starting-point)
  - [app/\_\_init\_\_.py — The App Factory](#2-app__init__py--the-app-factory)
  - [app/models.py — The Database Layer](#3-appmodelspy--the-database-layer)
  - [app/routes/auth.py — Login & Signup](#4-approutesauthpy--login--signup)
  - [app/routes/main.py — Core App Routes](#5-approutesmainpy--core-app-routes)
  - [app/services/emotion.py — The AI Brain](#6-appservicesemotionpy--the-ai-brain)
  - [app/templates/ — The HTML Pages](#7-apptemplates--the-html-pages)
  - [app/static/js/dashboard.js — The Live Camera Logic](#8-appstaticjsdashboardjs--the-live-camera-logic)
  - [web_model/ — The AI Model Files](#9-web_model--the-ai-model-files)
  - [requirements.txt — The Shopping List](#10-requirementstxt--the-shopping-list)
- [How Everything Connects (Step-by-Step Flow)](#-how-everything-connects-step-by-step-flow)
- [Setup & Installation](#-setup--installation)
- [Running the App](#-running-the-app)
- [Common Errors & Fixes](#-common-errors--fixes)

---

## 🎯 What Does This Project Do?

1. You **open the app** in your browser and **sign up / log in**
2. Your **webcam turns on** and starts capturing your face
3. Every **0.3 seconds**, a snapshot of your face is sent to the server
4. The server uses an **AI model** to detect your face and analyze your emotion
5. The result (e.g., "Happy 😊") is sent back and displayed on screen **in real-time**
6. The **background color changes** based on your emotion (yellow for happy, blue for sad, etc.)
7. Your **emotion history** is saved in a database

---

## 🧠 How It Works (The Big Picture)

Think of the project as having **3 layers**, like a sandwich:

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                   │
│  HTML pages + JavaScript                                │
│  • Shows the webcam feed                                │
│  • Captures frames and sends them to the server         │
│  • Displays the detected emotion with emoji & colors    │
├─────────────────────────────────────────────────────────┤
│                    BACKEND (Flask Server)                │
│  Python + Flask                                         │
│  • Receives image frames from the browser               │
│  • Passes them to the AI model for analysis             │
│  • Handles user login/signup                            │
│  • Sends results back to the browser                    │
├─────────────────────────────────────────────────────────┤
│                    AI MODEL (FER + TensorFlow)           │
│  Deep Learning                                          │
│  • Detects faces in the image (using MTCNN)             │
│  • Classifies the emotion on each face                  │
│  • Returns scores for all 7 emotions                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Technologies Used

| Technology       | What It Does                                        | Why We Use It                              |
| ---------------- | --------------------------------------------------- | ------------------------------------------ |
| **Python 3**     | The main programming language                       | Easy to learn, huge AI/ML ecosystem        |
| **Flask**        | Web framework (creates the server)                  | Lightweight, simple, perfect for small apps |
| **SQLite**       | Database (stores users & emotion logs)              | No setup needed, built into Python         |
| **TensorFlow**   | Machine learning framework                          | Powers the AI model that detects emotions  |
| **FER**          | Facial Emotion Recognition library                  | Pre-trained model — no training needed!    |
| **OpenCV**       | Computer vision library                             | Processes images (decode, resize, convert) |
| **MTCNN**        | Face detection neural network                       | Accurately finds faces in images           |
| **NumPy**        | Math/array library                                  | Handles image data as number arrays        |
| **Jinja2**       | HTML template engine (comes with Flask)             | Lets us put Python variables in HTML       |
| **TailwindCSS**  | CSS framework (loaded via CDN)                      | Makes the UI look modern with utility classes |
| **JavaScript**   | Frontend scripting language                         | Controls the webcam and sends data to server |
| **Werkzeug**     | Password hashing (comes with Flask)                 | Securely stores passwords                  |

---

## 📁 Project Structure (File Map)

Here's every important file and what it does:

```
emotion-analyzer/
│
├── run.py                        # 🚀 START HERE — launches the server
├── requirements.txt              # 📦 List of Python packages to install
├── users.db                      # 🗄️  SQLite database (auto-created)
│
├── app/                          # 📂 Main application folder
│   ├── __init__.py               # 🏗️  Creates and configures the Flask app
│   ├── models.py                 # 🗃️  Database models (User, EmotionLog)
│   │
│   ├── routes/                   # 🛤️  URL handlers (what happens when you visit a page)
│   │   ├── __init__.py           #     (empty — marks this as a Python package)
│   │   ├── auth.py               # 🔐 Login, Signup, Logout
│   │   └── main.py               # 🏠 Home page, Dashboard, Emotion API
│   │
│   ├── services/                 # ⚙️  Business logic
│   │   ├── __init__.py           #     (empty — marks this as a Python package)
│   │   └── emotion.py            # 🧠 THE AI — face detection & emotion analysis
│   │
│   ├── templates/                # 🖼️  HTML pages (rendered by Flask)
│   │   ├── base.html             # 📄 Base layout (shared by all pages)
│   │   ├── landing.html          # 🏠 Home/welcome page
│   │   ├── auth.html             # 🔐 Login & Signup form
│   │   └── dashboard.html        # 📊 Main app — webcam + emotion display
│   │
│   └── static/                   # 📁 Static files (JS, CSS, images)
│       └── js/
│           └── dashboard.js      # 🎥 Webcam capture + real-time updates
│
└── web_model/                    # 🤖 Pre-trained AI model files
    ├── model.json                #     Model architecture (structure)
    └── group1-shard1of1.bin      #     Model weights (the learned knowledge)
```

---

## 📝 Understanding Each File

### 1. `run.py` — The Starting Point

**📍 Location:** [run.py](file:///c:/emotion-detection/emotion-analyzer/run.py)

This is the **first file that runs** when you type `python run.py`. Think of it as the **ignition key** for your car.

**What it does:**
- Suppresses noisy warning messages from TensorFlow (so your terminal stays clean)
- Imports and creates the Flask app
- Starts the web server on **port 8080**

**Key lines explained:**
```python
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'     # Tell TensorFlow: "don't print warnings"
app = create_app()                             # Build the Flask application
app.run(host='0.0.0.0', port=8080)            # Start server, accessible on any network
```

> **💡 Beginner Tip:** `host='0.0.0.0'` means the server listens on ALL network interfaces — so you can access it from other devices on the same Wi-Fi (like your phone). If you only want localhost, you'd use `'127.0.0.1'`.

---

### 2. `app/__init__.py` — The App Factory

**📍 Location:** [\_\_init\_\_.py](file:///c:/emotion-detection/emotion-analyzer/app/__init__.py)

This file **builds the Flask app**. It's called a "factory" because it *creates* the app object.

**What it does:**
1. Creates a Flask application instance
2. Sets a secret key (needed for user sessions/cookies)
3. Registers **routes** (URL handlers) — so Flask knows what to do when you visit `/login`, `/dashboard`, etc.
4. Creates the **database tables** if they don't exist yet

**Database tables created:**
```
┌─────────────────────────────┐    ┌──────────────────────────────────┐
│         user                │    │         emotion_log              │
├─────────────────────────────┤    ├──────────────────────────────────┤
│ id (auto-increment)         │    │ id (auto-increment)              │
│ username (unique)           │◄───│ user_id (links to user)          │
│ password_hash (encrypted)   │    │ emotion ("happy", "sad", etc.)   │
│                             │    │ confidence (0.0 to 1.0)          │
│                             │    │ timestamp (when it was detected) │
└─────────────────────────────┘    └──────────────────────────────────┘
```

> **💡 Beginner Tip:** `__init__.py` is a special Python file. When you put it inside a folder, Python treats that folder as a **package** (a collection of modules you can import).

---

### 3. `app/models.py` — The Database Layer

**📍 Location:** [models.py](file:///c:/emotion-detection/emotion-analyzer/app/models.py)

This file handles **all database operations**. Instead of writing SQL queries everywhere, you call clean Python methods.

**Two classes:**

| Class | Purpose | Methods |
|-------|---------|---------|
| `User` | Manage user accounts | `create()` — register new user |
| | | `get_by_username()` — find user for login |
| | | `get_by_id()` — find user by ID |
| `EmotionLog` | Store emotion history | `create()` — save a detected emotion |
| | | `get_recent()` — get last 20 detections |

**Example flow:**
```
User signs up → User.create("alice", "hashed_password") → Saved to users.db
User logs in  → User.get_by_username("alice") → Returns user data
Emotion detected → EmotionLog.create(user_id=1, emotion="happy", confidence=0.95)
```

---

### 4. `app/routes/auth.py` — Login & Signup

**📍 Location:** [auth.py](file:///c:/emotion-detection/emotion-analyzer/app/routes/auth.py)

Handles **user authentication** — creating accounts and logging in.

**Routes (URLs):**

| URL | Method | What Happens |
|-----|--------|--------------|
| `/signup` | GET | Shows the signup form |
| `/signup` | POST | Creates a new user account |
| `/login` | GET | Shows the login form |
| `/login` | POST | Checks credentials and logs user in |
| `/logout` | GET | Clears session and logs user out |

**Security:** Passwords are **never stored as plain text**. They're hashed using `werkzeug.security`:
```
"mypassword123" → "pbkdf2:sha256:260000$abc123..." (one-way hash, can't be reversed)
```

---

### 5. `app/routes/main.py` — Core App Routes

**📍 Location:** [main.py](file:///c:/emotion-detection/emotion-analyzer/app/routes/main.py)

The **heart of the app** — handles the main pages and the emotion detection API.

**Routes:**

| URL | Method | What Happens |
|-----|--------|--------------|
| `/` | GET | Landing page (or redirects to dashboard if logged in) |
| `/dashboard` | GET | The main app page with webcam |
| `/detect_emotion` | POST | **API endpoint** — receives an image, returns the detected emotion |
| `/api/history` | GET | Returns the user's recent emotion history as JSON |

**The `/detect_emotion` flow (the most important route):**
```
Browser sends image (base64) → Flask receives it → emotion.py analyzes it
→ Result saved to database → JSON response sent back to browser
```

---

### 6. `app/services/emotion.py` — The AI Brain 🧠

**📍 Location:** [emotion.py](file:///c:/emotion-detection/emotion-analyzer/app/services/emotion.py)

This is where the **magic happens** — the AI that detects emotions!

**How it works, step by step:**

```
1. Receive base64 image string from the browser
       ↓
2. Decode base64 → raw bytes
       ↓
3. Convert bytes → NumPy array (a grid of numbers)
       ↓
4. Decode array → OpenCV image (actual picture with pixels)
       ↓
5. FER detector analyzes the image:
   a. MTCNN finds all faces in the image (draws boxes around them)
   b. For each face, the neural network predicts 7 emotion scores
       ↓
6. Return the dominant emotion + all scores
```

**Example output from the AI model:**
```python
{
    'angry': 0.02,
    'disgust': 0.01,
    'fear': 0.03,
    'happy': 0.85,    # ← Highest! This is the dominant emotion
    'sad': 0.04,
    'surprise': 0.03,
    'neutral': 0.02
}
# Result: "happy" with 85% confidence
```

> **💡 Beginner Tip:** FER uses a pre-trained model — meaning someone already trained it on thousands of facial images. You don't need to train it yourself! `mtcnn=True` uses a more accurate (but slower) face detection method.

---

### 7. `app/templates/` — The HTML Pages

These are the **visual pages** users see in their browser. They use **Jinja2 templating** — a way to mix Python variables into HTML.

#### `base.html` — [Base Layout](file:///c:/emotion-detection/emotion-analyzer/app/templates/base.html)
The **parent template** that all other pages inherit from. Contains:
- The `<head>` section (TailwindCSS, Google Fonts)
- A dark purple gradient background
- A glassmorphism effect (`.glass` class)
- Flash message display (notifications)

#### `landing.html` — [Landing Page](file:///c:/emotion-detection/emotion-analyzer/app/templates/landing.html)
The **welcome page** visitors see first. Features:
- Animated gradient title
- "Get Started" and "Login" buttons
- Three feature cards (Real-Time, Private, Accurate)

#### `auth.html` — [Login/Signup Page](file:///c:/emotion-detection/emotion-analyzer/app/templates/auth.html)
A **single page** that handles both login and signup (switched using the `mode` variable). Features:
- Animated gradient blob backgrounds
- Glassmorphism card design
- Lucide icons for the input fields
- Google sign-in button (UI only)

#### `dashboard.html` — [Dashboard](file:///c:/emotion-detection/emotion-analyzer/app/templates/dashboard.html)
The **main app page** after login. Contains:
- Live webcam video feed (mirrored like a selfie camera)
- Loading spinner while camera initializes
- Pause/Resume button (appears on hover)
- Emotion card showing the current emoji + emotion label

> **💡 Beginner Tip:** `{% extends "base.html" %}` means "use base.html as my layout, and put my content inside the `{% block content %}` area."

---

### 8. `app/static/js/dashboard.js` — The Live Camera Logic

**📍 Location:** [dashboard.js](file:///c:/emotion-detection/emotion-analyzer/app/static/js/dashboard.js)

This JavaScript file runs **in the browser** and controls the entire real-time experience.

**What it does:**

1. **Starts the webcam** using the browser's `getUserMedia` API
2. **Captures a frame** every 300ms (0.3 seconds) by drawing the video to a hidden `<canvas>`
3. **Converts the frame** to a base64 JPEG image
4. **Sends it to the server** via `fetch('/detect_emotion', ...)`
5. **Receives the emotion** back from the server
6. **Smooths the results** — uses a buffer of the last 5 readings and picks the most frequent emotion (prevents flickering)
7. **Updates the UI** — changes the emoji, label, background color, and card border

**The emotion-to-visual mapping:**
```
😐 Neutral  → Dark gray background
😊 Happy    → Yellow/orange gradient
😔 Sad      → Blue/indigo gradient
😠 Angry    → Red/rose gradient
😨 Fearful  → Purple/violet gradient
🤢 Disgusted → Green/emerald gradient
😲 Surprised → Pink/fuchsia gradient
```

---

### 9. `web_model/` — The AI Model Files

**📍 Location:** [web_model/](file:///c:/emotion-detection/emotion-analyzer/web_model)

These are the **pre-trained neural network model files** in TensorFlow.js format:

- **`model.json`** — The model's **architecture** (what layers it has, how they connect). Think of this as the **blueprint** of a building.
- **`group1-shard1of1.bin`** — The model's **weights** (the learned numbers). Think of this as the **furniture and contents** inside the building.

---

### 10. `requirements.txt` — The Shopping List

**📍 Location:** [requirements.txt](file:///c:/emotion-detection/emotion-analyzer/requirements.txt)

Lists every Python **package** (library) this project needs:

| Package | What It Does |
|---------|-------------|
| `flask` | Web server framework |
| `opencv-python` | Image processing (decode, resize, color convert) |
| `numpy` | Array/matrix math for image data |
| `requests` | HTTP requests (for downloading models, etc.) |
| `fer` | Facial Emotion Recognition — the pre-trained AI model |
| `tensorflow` | The deep learning engine that powers the AI model |
| `tf-keras` | Keras API for TensorFlow (model layers & training) |

---

## 🔄 How Everything Connects (Step-by-Step Flow)

Here's the complete journey from opening the app to seeing an emotion:

```
                            ┌──────────────────┐
                            │  User opens       │
                            │  localhost:8080   │
                            └────────┬─────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                    ┌─NO─│  Logged in?           │─YES─┐
                    │    └───────────────────────┘     │
                    ▼                                   ▼
           ┌────────────────┐                  ┌────────────────┐
           │  landing.html  │                  │ dashboard.html │
           │  (Welcome page)│                  │ (Main app)     │
           └───────┬────────┘                  └───────┬────────┘
                   │                                   │
                   ▼                                   ▼
           ┌────────────────┐                  ┌────────────────┐
           │   auth.html    │                  │  dashboard.js  │
           │ (Login/Signup) │                  │  starts webcam │
           └───────┬────────┘                  └───────┬────────┘
                   │                                   │
                   ▼                                   ▼ (every 0.3s)
           ┌────────────────┐                  ┌────────────────┐
           │   auth.py      │                  │  Capture frame │
           │  checks creds  │                  │  as base64     │
           └───────┬────────┘                  └───────┬────────┘
                   │                                   │
                   ▼                                   ▼
           ┌────────────────┐                  ┌────────────────┐
           │   models.py    │                  │  POST /detect  │
           │  User.create() │                  │  _emotion      │
           │  or verify     │                  └───────┬────────┘
           └────────────────┘                          │
                                                       ▼
                                               ┌────────────────┐
                                               │  main.py route │
                                               │  receives image│
                                               └───────┬────────┘
                                                       │
                                                       ▼
                                               ┌────────────────┐
                                               │  emotion.py    │
                                               │  FER + MTCNN   │
                                               │  analyzes face │
                                               └───────┬────────┘
                                                       │
                                                       ▼
                                               ┌────────────────┐
                                               │  Returns JSON: │
                                               │  {emotion:     │
                                               │   "happy",     │
                                               │   details:{..}}│
                                               └───────┬────────┘
                                                       │
                                                       ▼
                                               ┌────────────────┐
                                               │  dashboard.js  │
                                               │  updates emoji,│
                                               │  label, colors │
                                               └────────────────┘
```

---

## ⚡ Setup & Installation

### Prerequisites

- **Python 3.10+** installed ([download here](https://www.python.org/downloads/))
- A **webcam** (built-in laptop camera works fine)
- A modern **web browser** (Chrome, Firefox, Edge)

### Step 1: Clone or Download the Project

```bash
git clone <your-repo-url>
cd emotion-analyzer
```

### Step 2: Create a Virtual Environment

A virtual environment keeps this project's packages separate from your system Python.

```bash
# Create the virtual environment
python -m venv .venv

# Activate it
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# On Windows (CMD):
.\.venv\Scripts\activate.bat

# On macOS/Linux:
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> **⚠️ Python 3.12+ users:** If you get a `ModuleNotFoundError: No module named 'pkg_resources'` error, run:
> ```bash
> pip install "setuptools<81"
> ```

### Step 4: Verify Installation

```bash
python -c "from fer.fer import FER; print('All good!')"
```

---

## 🚀 Running the App

```bash
python run.py
```

You should see:
```
Starting Emotion Analyzer...
Go to http://0.0.0.0:8080 (or your Pi's IP address)
 * Serving Flask app 'app'
 * Debug mode: on
```

Open your browser and go to: **http://localhost:8080**

---

## 🔧 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'pkg_resources'` | setuptools v84+ removed pkg_resources | `pip install "setuptools<81"` |
| `Camera Access Denied` in browser | Browser blocked webcam | Click the camera icon in the URL bar and allow access |
| `No module named 'cv2'` | OpenCV not installed | `pip install opencv-python` |
| `No module named 'tensorflow'` | TensorFlow not installed | `pip install tensorflow` |
| Server not accessible from phone | Firewall blocking port | Allow port 8080 through Windows Firewall |

---

## 📄 License

This project is for educational purposes.

---

> **Built with ❤️ using Python, Flask, TensorFlow, and FER**
