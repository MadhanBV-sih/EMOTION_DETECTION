# Running Calm Mirror on Raspberry Pi 5

Your Raspberry Pi 5 is more than capable of running this application. Since the AI processing happens in the user's browser, the Pi only needs to serve the web pages.

## 1. Preparation
Transfer this project folder to your Raspberry Pi.

## 2. Installation (Lightweight)
You do **not** need to install heavy libraries like TensorFlow or OpenCV just to run the website.

Open a terminal in the project folder on your Pi and run:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install ONLY the web server requirements
pip install -r requirements-rpi.txt
```

## 3. Running the Server
Start the application:

```bash
python app.py
```

## 4. Accessing from other devices
By default, the server runs on `127.0.0.1` (localhost). To access it from your phone or laptop:

1.  **Find your Pi's IP address**: Run `hostname -I` in the terminal (e.g., `192.168.1.15`).
2.  **Modify `app.py`** (Optional):
    Change the last line in `app.py` to listen on all interfaces:
    ```python
    app.run(debug=True, host='0.0.0.0', port=5000)
    ```
3.  **Open in Browser**:
    Go to `http://<YOUR_PI_IP>:5000` (e.g., `http://192.168.1.15:5000`).

## Troubleshooting
-   **Camera Issues**: Ensure the device *viewing* the webpage has a webcam. The Pi does not need a camera connected to it.
-   **HTTPS**: Modern browsers require HTTPS for camera access if not on `localhost`. If you can't open the camera on your phone, you may need to set up a simple HTTPS tunnel (like `ngrok`) or trust the insecure origin in your browser settings.
