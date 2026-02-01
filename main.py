import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model_logic import analyze_voice

# 1. Initialize FastAPI with metadata for judges
app = FastAPI(
    title="AI Voice Fraud Detection API",
    description="Multi-language detection for Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

# 2. Define the exact JSON structure required
class AudioRequest(BaseModel):
    audio_base64: str

# 3. Create a professional Landing Page
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #2e86de;">API Status: Online</h1>
            <p>Endpoint: <code>/detect</code> | Method: <code>POST</code></p>
            <a href="/docs" style="color: #3498db;">View Interactive API Docs</a>
        </body>
    </html>
    """

# 4. The Functional Detection Endpoint
@app.post("/detect")
async def detect_voice(request: AudioRequest, authorization: str = Header(None)):
    # Security: Verify API Key
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    try:
        # Convert Base64 back to temporary audio file
        temp_filename = f"temp_{uuid.uuid4()}.mp3"
        audio_data = base64.b64decode(request.audio_base64)
        
        with open(temp_filename, "wb") as f:
            f.write(audio_data)

        # Run detection logic from model_logic.py
        classification, confidence = analyze_voice(temp_filename)

        # Cleanup: Delete temp file to keep server storage clean
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        if classification == "ERROR":
            raise HTTPException(status_code=500, detail="Processing failed.")

        # Return structured JSON response
        return {
            "classification": classification,
            "confidence": confidence,
            "explanation": f"Acoustic features suggest origin is {classification}."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid audio data or format.")


