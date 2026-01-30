import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from model_logic import analyze_voice

app = FastAPI()

class AudioRequest(BaseModel):
    audio_base64: str

@app.post("/detect")
async def detect(request: AudioRequest, authorization: str = Header(None)):
    # Hackathon requirement: Authorization check
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing API Key")

    try:
        # Create unique temp file to avoid multi-user conflicts
        temp_filename = f"audio_{uuid.uuid4()}.mp3"
        audio_bytes = base64.b64decode(request.audio_base64)
        
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)

        # Process
        result, score = analyze_voice(temp_filename)

        # Cleanup file immediately
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        if result == "ERROR":
            raise HTTPException(status_code=500, detail="Audio analysis failed. Ensure MP3 format.")

        return {
            "classification": result,
            "confidence": score,
            "explanation": "Signal processed for spectral flatness and MFCC variance."
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid audio data")

@app.get("/")
def health():
    return {"status": "Live"}
