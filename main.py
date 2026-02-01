import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model_logic import analyze_voice

# The 'info' section is generated here
app = FastAPI(
    title="Multi-Language AI Voice Detector",
    description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

class AudioRequest(BaseModel):
    audio_base64: str

# --- INCLUDED IN SCHEMA ---
@app.get(
    "/", 
    response_class=HTMLResponse, 
    summary="Root", 
    operation_id="root__get",
    responses={200: {"description": "Successful Response"}}
)
async def root():
    return "<html><body><h1>API Active</h1></body></html>"

# --- HIDDEN FROM SCHEMA ---
@app.post(
    "/detect", 
    include_in_schema=False  # Hides the route and its models from openapi.json
)
async def detect(request: AudioRequest, authorization: str = Header(None)):
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


