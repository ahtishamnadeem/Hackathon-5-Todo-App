"""
Hugging Face Spaces entry point for FastAPI application.
"""
import os
from app.main import app

# Hugging Face Spaces uses PORT environment variable (default 7860)
port = int(os.getenv("PORT", 7860))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
