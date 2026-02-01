import base64
import os
import uuid
import requests
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

# Import your logic from model_logic.py
from model_logic import analyze_voice

app = FastAPI(
    title="Multi-Language AI Voice Detector",
    description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

# This model handles both Base64 (from your script) and URLs (from judges)
class AudioRequest(BaseModel):
    audio_base64: Optional[str] = None
    audio_url: Optional[str] = None

@app.get("/", response_class=HTMLResponse, summary="Root", operation_id="root__get")
async def root():
    return "<html><body><h1>API Active: Submit POST to /detect</h1></body></html>"

@app.post("/detect", include_in_schema=False)
async def detect(request: AudioRequest, authorization: str = Header(None)):
    # 1. Security Check
    if authorization != "HACKATHON_TEST_KEY":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    temp_filename = f"audio_{uuid.uuid4()}.mp3"
    
    try:
        # 2. Handle Audio Input (Base64 vs URL)
        if request.audio_base64:
            audio_bytes = base64.b64decode(request.audio_base64)
            with open(temp_filename, "wb") as f:
                f.write(audio_bytes)
        elif request.audio_url:
            response = requests.get(request.audio_url, timeout=10)
            with open(temp_filename, "wb") as f:
                f.write(response.content)
        else:
            raise HTTPException(status_code=400, detail="No audio source provided")

        # 3. Run your model_logic.py analysis
        result, score = analyze_voice(temp_filename)

        # 4. Return the structured JSON judges expect
        return {
            "classification": result,
            "confidence": score,
            "explanation": f"Acoustic feature variance is {score} (Multi-language check)."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    
    finally:
        # Always delete temp files to avoid filling up Render's disk
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


