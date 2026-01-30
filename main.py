import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model_logic import analyze_voice

# The metadata here generates the 'info' section of your openapi.json
app = FastAPI(
    title="Multi-Language AI Voice Detector",
    description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

# Required for the POST request body
class AudioRequest(BaseModel):
    audio_base64: str

# --- GET ROUTE ---
# This matches your requested 'root__get' operationId
@app.get("/", response_class=HTMLResponse, operation_id="root__get")
async def root():
    """
    Root endpoint that returns a simple HTML landing page.
    """
    return """
    <html>
        <head><title>AI Voice Detector</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #2e86de;">AI Voice Detection System Live</h1>
            <p>Supported Languages: Tamil, Hindi, English, Telugu, Malayalam</p>
            <div style="margin-top: 20px;">
                <a href="/docs" style="padding: 10px 20px; background: #2e86de; color: white; text-decoration: none; border-radius: 5px;">View API Documentation</a>
            </div>
        </body>
    </html>
    """

# --- POST ROUTE ---
@app.post("/detect", operation_id="detect_voice__post")
async def detect(request: AudioRequest, authorization: str = Header(None)):
    # Your specific API Key from test_api.py
    if authorization != "HACKATHON_TEST_KEY":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        # Process the audio
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
        raise HTTPException(status_code=400, detail="Invalid audio format")



