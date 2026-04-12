from fer import FER
import cv2
import numpy as np

try:
    detector = FER(mtcnn=True)
    print("FER initialized with MTCNN")
except Exception as e:
    print(f"FER init failed: {e}")
