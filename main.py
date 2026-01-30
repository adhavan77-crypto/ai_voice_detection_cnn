import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model_logic import analyze_voice

# The 'info' section of your openapi.json is generated from these parameters
app = FastAPI(
    title="Multi-Language AI Voice Detector",
    description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

# This defines the JSON body for the POST /detect endpoint
class AudioRequest(BaseModel):
    audio_base64: str

# 1. GET ROUTE: Matches your required operationId and 200 description
@app.get(
    "/", 
    response_class=HTMLResponse, 
    summary="Root", 
    operation_id="root__get",
    responses={200: {"description": "Successful Response"}}
)
async def root():
    return """
    <html>
        <head><title>AI Voice Detector</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>AI Voice Detection System Live</h1>
            <p>Supported Languages: Tamil, Hindi, English, Telugu, Malayalam</p>
            <a href="/docs">View API Documentation</a>
        </body>
    </html>
    """

# 2. POST ROUTE: Handles the actual detection
@app.post(
    "/detect", 
    summary="Detect", 
    operation_id="detect_voice__post"
)
async def detect(request: AudioRequest, authorization: str = Header(None)):
    # Security check matching your test_api.py
    if authorization != "HACKATHON_TEST_KEY":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        temp_filename = f"audio_{uuid.uuid4()}.mp3"
        audio_bytes = base64.b64decode(request.audio_base64)
        
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)

        result, score = analyze_voice(temp_filename)
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        return {
            "classification": result,
            "confidence": score,
            "explanation": f"Acoustic features analyzed (Result: {result})."
        }
    except Exception:
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=400, detail="Invalid audio format")




