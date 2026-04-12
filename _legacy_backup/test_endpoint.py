import requests
import base64
import numpy as np
import cv2
import json

# Create a dummy image
img = np.zeros((480, 640, 3), dtype=np.uint8)
# Draw a white circle to simulate a face (won't be detected but endpoint should run)
cv2.circle(img, (320, 240), 100, (255, 255, 255), -1)

_, buffer = cv2.imencode('.jpg', img)
img_str = base64.b64encode(buffer).decode('utf-8')

url = 'http://127.0.0.1:5000/detect_emotion'
payload = {'image': img_str}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
