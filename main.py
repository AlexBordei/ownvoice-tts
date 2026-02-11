"""
OwnVoice TTS Server
A simple Text-to-Speech server supporting Romanian and multiple languages
"""

import os
import logging
from pathlib import Path
from typing import Optional
import hashlib
from datetime import datetime

from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="OwnVoice TTS Server",
    description="Text-to-Speech server with Romanian support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create cache directory
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Supported languages
LANGUAGES = {
    "ro": {"name": "Romanian", "tld": "com"},
    "ro-f": {"name": "Romanian (Female)", "tld": "com"},  # Alias for ro
    "en": {"name": "English", "tld": "com"},
    "es": {"name": "Spanish", "tld": "com"},
    "fr": {"name": "French", "tld": "com"},
    "de": {"name": "German", "tld": "com"},
    "it": {"name": "Italian", "tld": "com"},
    "pt": {"name": "Portuguese", "tld": "com"},
}


def generate_cache_key(text: str, lang: str) -> str:
    """Generate a unique cache key for text and language"""
    content = f"{text}_{lang}"
    return hashlib.md5(content.encode()).hexdigest()


def get_cached_audio(cache_key: str) -> Optional[Path]:
    """Check if audio is already cached"""
    audio_path = CACHE_DIR / f"{cache_key}.mp3"
    if audio_path.exists():
        logger.info(f"Cache hit for key: {cache_key}")
        return audio_path
    return None


@app.post("/synthesize")
async def synthesize(
    text: str = Form(...),
    lang: str = Form(default="ro"),
    voice: Optional[str] = Form(default=None)
):
    """
    Synthesize text to speech

    Args:
        text: Text to synthesize
        lang: Language code (ro, en, es, fr, de, it, pt)
        voice: Voice ID (optional, not used with gTTS)

    Returns:
        Audio file (MP3 format)
    """
    try:
        logger.info(f"Synthesize request - Text: '{text[:50]}...', Lang: {lang}")

        # Validate text
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Normalize language code
        if lang == "ro-f":
            lang = "ro"  # gTTS doesn't distinguish male/female for Romanian

        # Validate language
        if lang not in LANGUAGES and lang != "ro-f":
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {lang}. Supported: {', '.join(LANGUAGES.keys())}"
            )

        # Check cache
        cache_key = generate_cache_key(text, lang)
        cached_audio = get_cached_audio(cache_key)

        if cached_audio:
            logger.info(f"Returning cached audio: {cached_audio}")
            return FileResponse(
                path=str(cached_audio),
                media_type="audio/mpeg",
                filename=f"speech_{cache_key}.mp3"
            )

        # Generate new audio
        audio_path = CACHE_DIR / f"{cache_key}.mp3"

        logger.info(f"Generating new audio with gTTS...")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(audio_path))

        logger.info(f"Audio generated successfully: {audio_path}")

        return FileResponse(
            path=str(audio_path),
            media_type="audio/mpeg",
            filename=f"speech_{cache_key}.mp3"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    cache_files = len(list(CACHE_DIR.glob("*.mp3")))

    return {
        "status": "healthy",
        "service": "OwnVoice TTS",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "cache": {
            "directory": str(CACHE_DIR),
            "files": cache_files
        },
        "supported_languages": len(LANGUAGES)
    }


@app.get("/languages")
async def languages():
    """List supported languages"""
    return {
        "languages": [
            {
                "code": code,
                "name": info["name"]
            }
            for code, info in LANGUAGES.items()
        ]
    }


@app.get("/voices")
async def voices():
    """List available voices (gTTS uses default voices per language)"""
    return {
        "voices": [
            {
                "id": code,
                "name": f"{info['name']} (Default)",
                "language": code
            }
            for code, info in LANGUAGES.items()
        ]
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OwnVoice TTS Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "synthesize": "POST /synthesize",
            "health": "GET /health",
            "languages": "GET /languages",
            "voices": "GET /voices"
        }
    }


if __name__ == "__main__":
    # Run the server
    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")

    logger.info(f"Starting OwnVoice TTS Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
