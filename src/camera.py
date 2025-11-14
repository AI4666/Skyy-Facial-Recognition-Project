# src/camera.py
import cv2
import numpy as np
from typing import Optional

class CameraManager:
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.cap = cv2.VideoCapture(self.device_id)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera device {self.device_id}")
            self.cap = None
            
    def capture_image(self) -> Optional[np.ndarray]:
        """
        Captures a single frame from the camera.
        Corresponds to FR-1.1 
        """
        if not self.cap or not self.cap.isOpened():
            print("Camera is not available.")
            return None
            
        ret, frame = self.cap.read()
        
        if not ret:
            print("Failed to capture image.")
            return None
            
        # Per FR-1.1.3, system shall capture RGB format. OpenCV uses BGR.
        # The facial_recognition.py module expects BGR, so we'll pass it as is.
        # If another module needed RGB, we'd use: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def __del__(self):
        if self.cap:
            self.cap.release()

# Singleton instance
cam_manager = CameraManager()