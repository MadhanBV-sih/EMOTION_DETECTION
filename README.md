# Emotion Analyzer

> **Real-Time Facial Emotion Recognition Engine**

A high-performance emotion recognition system built with deep learning and computer vision.  
**Emotion Analyzer** detects facial emotions in real time, logs session data, and presents insights through a secure analytics dashboard. Designed for reliability, performance, and edge deployment.

---

## Overview

Most emotion-detection projects stop at a demo.  
**Emotion Analyzer is built as a complete system.**

It combines real-time inference, user authentication, data persistence, and analytics into a single, deployable application that runs efficiently on both local machines and low-power devices like Raspberry Pi.

*Use cases include research, HCI systems, emotion-aware applications, and edge AI deployments.*

## Features

🚀 **Real-time facial emotion detection** via webcam  
🧠 **CNN-based deep learning model** (FER)  
🛡️ **Secure login and registration system**  
📊 **Session-based emotion logging**  
📈 **Analytics dashboard** for emotion trends  
⚡ **Lightweight and edge-device friendly**

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **Backend** | Flask |
| **ML / DL** | TensorFlow (CNN) |
| **Computer Vision** | OpenCV |
| **Database** | SQLite |
| **Frontend** | Jinja2, HTML, CSS |
| **Deployment** | Local, Edge, IoT |

## Project Structure

```bash
.
├── app
│   ├── routes/          # API and view controllers
│   ├── services/        # Core logic and ML models
│   ├── static/          # Frontend assets
│   ├── templates/       # Jinja2 templates
│   ├── models.py        # Database models
│   └── __init__.py      # Flask app factory
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
└── RPI_SETUP.md         # Raspberry Pi deployment guide
```

*Clean separation of concerns. No monoliths. No shortcuts.*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/emotion-analyzer.git
cd emotion-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python run.py
```

> **Open in browser:** `http://localhost:8080`

## How It Works

1.  **Webcam frames** captured using OpenCV.
2.  **Face detection and normalization** in real time.
3.  **CNN model** predicts emotion class.
4.  **Emotion data** logged per user session.
5.  **Dashboard** visualizes emotion distributions and trends.

*Offline-first. Low latency. No cloud dependency.*

## Security

*   🔒 Passwords stored using hashing.
*   👤 User sessions isolated.
*   🚫 No third-party data sharing.
*   🌐 Fully offline-capable deployment.

## Performance

*   ⚡ Real-time CPU inference.
*   🫐 Raspberry Pi compatible.
*   💾 Low memory footprint.
*   🔄 Model can be swapped or upgraded without refactoring core logic.

## Roadmap

- [ ] Cloud synchronization and user profiles
- [ ] REST API with OpenAPI documentation
- [ ] Mobile application integration
- [ ] Emotion reports (PDF / CSV)
- [ ] Multi-modal sentiment analysis (face + voice + text)

## Contributing

Contributions are welcome. Relevant areas include:

*   Computer Vision
*   Emotion AI
*   Edge AI / IoT
*   Human–Computer Interaction

## License

MIT License
