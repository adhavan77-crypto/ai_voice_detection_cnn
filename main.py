import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

# Import the logic from your model_logic.py file
from model_logic import analyze_voice

app = FastAPI(title="AI Voice Detection API")

# This matches the structure in your test_api.py payload
class AudioRequest(BaseModel):
    audio_base64: str

# Define your secret key here
VALID_API_KEY = "HACKATHON_TEST_KEY"

@app.get("/")
async def health_check():
    return {"status": "Online", "message": "Send POST requests to /detect"}

@app.post("/detect")
async def detect_voice(request: AudioRequest, authorization: str = Header(None)):
    # 1. Check if the API Key matches HACKATHON_TEST_KEY
    if authorization != VALID_API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or missing Authorization header"
        )

    try:
        # 2. Decode the Base64 audio string
        # Your test_api.py sends a UTF-8 string, we convert it back to bytes
        audio_bytes = base64.b64decode(request.audio_base64)
        
        # 3. Save to a temporary file so librosa can read it
        temp_filename = f"temp_{uuid.uuid4()}.mp3"
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)

        # 4. Call your analyze_voice function from model_logic.py
        classification, confidence = analyze_voice(temp_filename)

        # 5. Clean up the temporary file immediately
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        # Handle errors from the model logic
        if classification == "ERROR":
            raise HTTPException(status_code=500, detail="Audio analysis failed")

        # 6. Return the JSON response in the required format
        return {
            "classification": classification,
            "confidence": confidence,
            "explanation": f"Analysis based on spectral characteristics (Result: {classification})"
        }

    except Exception as e:
        # Cleanup file if an error occurs during processing
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

# This ensures the app runs correctly on Render's port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)



