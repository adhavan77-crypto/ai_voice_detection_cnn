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
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing API Key")

    try:
        temp_filename = f"audio_{uuid.uuid4()}.mp3"
        audio_bytes = base64.b64decode(request.audio_base64)
        
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)

        result, score = analyze_voice(temp_filename)
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        if result == "ERROR":
            raise HTTPException(status_code=500, detail="Analysis failed.")

        return {
            "classification": result,
            "confidence": score,
            "explanation": f"Acoustic features analyzed (Result: {result})."
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid audio format")


