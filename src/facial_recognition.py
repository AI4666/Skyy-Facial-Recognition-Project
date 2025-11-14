# src/facial_recognition.py
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
from typing import Optional, List
from .config import config

# Load InsightFace configuration
MODEL_NAME = config['insightface']['model_name']
USE_GPU = config['insightface']['use_gpu']

class RecognitionService:
    def __init__(self):
        self.app = FaceAnalysis(name=MODEL_NAME)
        
        providers = ['CPUExecutionProvider']
        if USE_GPU:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            
        self.app.prepare(ctx_id=0, det_size=(640, 640), providers=providers)
        print("Facial RecognitionService initialized with InsightFace.")

    def get_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Detects a face and returns its 512-d embedding.
        Corresponds to FR-1.2 [cite: 9] and Recognition Flow [cite: 42]
        """
        # insightface expects BGR images, OpenCV reads in BGR by default
        faces = self.app.get(image)
        
        if not faces:
            print("No face detected.") # FR-1.2.4
            return None
            
        if len(faces) > 1:
            print("Multiple faces detected, processing primary (largest) face.") # FR-1.2.5
            # Sort by detection score or bounding box size, here we just take the first
            faces.sort(key=lambda x: (x.bbox[2]-x.bbox[0]) * (x.bbox[3]-x.bbox[1]), reverse=True)

        # Get the embedding from the first (or largest) face
        embedding = faces[0].normed_embedding
        return embedding

# Singleton instance
rec_service = RecognitionService()