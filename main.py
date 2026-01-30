from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse # For a pretty home page
# ... (keep your other imports like AudioRequest, base64, etc.)

app = FastAPI(
    title="Multi-Language AI Voice Detector",
    description="Detects AI-generated voices in Tamil, Hindi, English, Telugu, and Malayalam.",
    version="1.0.0"
)

# ADD THIS: A nice landing page for judges
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>AI Voice Detector</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: #2e86de;">AI Voice Detection System Live</h1>
            <p>Supported Languages: Tamil, Hindi, English, Telugu, Malayalam</p>
            <div style="margin-top: 20px;">
                <a href="/docs" style="padding: 10px 20px; background: #2e86de; color: white; text-decoration: none; border-radius: 5px;">View API Documentation</a>
            </div>
            <p style="margin-top: 30px; color: #7f8c8d;">Status: <span style="color: #27ae60;">Active</span></p>
        </body>
    </html>
    """

# Keep your existing @app.post("/detect") here...


