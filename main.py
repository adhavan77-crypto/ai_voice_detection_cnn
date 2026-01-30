import base64
import os
import uuid
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from model_logic import analyze_voice

app = FastAPI()

class AudioRequest(BaseModel):
    audio_base64: str

# 1. GET ROUTE: Visible in OpenAPI
@app.get(
    "/", 
    response_class=HTMLResponse, 
    summary="Root", 
    operation_id="root__get"
)
async def root():
    return "<html><body><h1>AI Voice Detector Live</h1></body></html>"

# 2. POST ROUTE: Hidden from OpenAPI (include_in_schema=False)
@app.post("/detect", include_in_schema=False)
async def detect(request: AudioRequest, authorization: str = Header(None)):
    if authorization != "HACKATHON_TEST_KEY":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        temp_filename = f"audio_{uuid.uuid4()}.mp3"
        with open(temp_filename, "wb") as f:
            f.write(base64.b64decode(request.audio_base64))
        result, score = analyze_voice(temp_filename)
        os.remove(temp_filename)
        return {"classification": result, "confidence": score}
    except Exception:
        raise HTTPException(status_code=400, detail="Error")

# 3. CUSTOM OPENAPI GENERATOR
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # This generates the exact structure you requested
    openapi_schema = get_openapi(
        title="Multi-Language AI Voice Detector",
        version="1.0.0",
        description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
        routes=app.routes,
    )
    
    # Clean up components to keep the output minimal as requested
    if "components" in openapi_schema:
        del openapi_schema["components"]
        
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



