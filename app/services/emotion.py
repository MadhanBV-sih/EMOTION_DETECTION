import cv2
import numpy as np
import base64
from fer.fer import FER
import logging

# Initialize FER detector
# mtcnn=True is more accurate but slower. Default is False (Haar Cascade) which is faster.
# We'll try default first for speed, can switch to mtcnn=True if accuracy is poor.
try:
    detector = FER(mtcnn=True)
except Exception as e:
    logging.warning(f"Failed to load MTCNN, falling back to default OpenCV Haarcascade: {e}")
    detector = FER()

def detect_emotion_from_frame(image_data):
    try:
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None, "Failed to decode image"

        # Detect emotions
        result = detector.detect_emotions(img)
        
        if not result:
            return "neutral", {"neutral": 1.0}
        
        # Get emotion from first face
        # FER returns: [{'box': (x, y, w, h), 'emotions': {'angry': 0.0, ...}}]
        face_emotions = result[0]['emotions']
        
        # Find dominant emotion
        dominant_emotion = max(face_emotions.items(), key=lambda x: x[1])[0]
        
        # FER returns 0.0 to 1.0 directly, just like we want
        return dominant_emotion, face_emotions
            
    except Exception as e:
        print(f"Error in detection: {e}")
        return None, str(e)
