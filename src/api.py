# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import base64
import cv2
import os
import uuid
import asyncio
import time

# Import our custom modules
from . import database, facial_recognition, camera
from .config import config

# Create the FastAPI app
app = FastAPI()

# --- Data Models for API requests/responses ---
# Based on 6.3.1 Sample MCP Request
class RecognizeRequest(BaseModel):
    image_data: Optional[str] = None # Base64 encoded image
    # if no image_data, will use local camera

# Based on 6.3.1 Sample MCP Response
class RecognitionResponse(BaseModel):
    user_id: str
    name: str
    confidence: float
    timestamp: str # Use datetime

class RegisterRequest(BaseModel):
    name: str

# --- API Endpoints (Implementing MCP Commands) ---

@app.post("/facial_recognition.recognize_user", response_model=RecognitionResponse)
async def recognize_user(request: RecognizeRequest):
    """
    Implements the 'facial_recognition.recognize_user' MCP command
    This follows Use Case 2
    """
    print("Received recognition request...")
    image = None
    if request.image_data:
        # Decode base64 image [cite: 31]
        img_bytes = base64.b64decode(request.image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    else:
        # Capture image from local camera [cite: 15]
        image = camera.cam_manager.capture_image()
        if image is None:
            raise HTTPException(status_code=500, detail="Failed to capture image from camera.")

    # 2. Get embedding
    embedding = facial_recognition.rec_service.get_embedding(image)
    if embedding is None:
        raise HTTPException(status_code=404, detail="No face detected in the image.")

    # 3. Search database
    user_data = database.db_manager.search_user(embedding.tolist())
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not recognized or confidence too low.")

    # 4. Return success response
    response = RecognitionResponse(
        user_id=user_data['user_id'],
        name=user_data['name'],
        confidence=user_data['confidence'],
        timestamp="ISO_TIMESTAMP_HERE" # Add datetime logic
    )
    return response


@app.post("/facial_recognition.register_user")
async def register_user(request: RegisterRequest):
    """
    Implements the 'facial_recognition.register_user' MCP command
    This follows Use Case 1
    """
    print(f"Received registration request for: {request.name}")
    
    # Per FR-2.3.1, capture 3-5 images
    capture_count = config['registration']['capture_count']
    embeddings = []
    captured_images = []

    for i in range(capture_count):
        print(f"Capture {i+1}/{capture_count}... Look at the camera.")
        # In a real app, you'd add delays and user prompts [cite: 49]
        image = camera.cam_manager.capture_image()
        if image is None:
            raise HTTPException(status_code=500, detail="Failed to capture image.")

        embedding = facial_recognition.rec_service.get_embedding(image)
        if embedding is None:
            raise HTTPException(status_code=400, detail=f"No face detected in capture {i+1}. Please try again.")
        
        embeddings.append(embedding.tolist())
        captured_images.append(image)
        await asyncio.sleep(1)
        

    # Save the *first* high-quality image as the profile image
    profile_image_filename = f"{str(uuid.uuid4())}.jpg"
    profile_image_path = os.path.join(config['storage']['image_storage_path'], profile_image_filename)
    cv2.imwrite(profile_image_path, captured_images[0])
    
    # Store in database
    user_id = database.db_manager.add_user(
        name=request.name,
        embeddings=embeddings,
        profile_image_path=profile_image_path
    )
    
    return {"message": f"User {request.name} registered successfully with ID {user_id}", "user_id": user_id}