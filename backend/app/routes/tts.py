"""
Text-to-Speech and Media handling endpoints
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
import os
import hashlib
import io
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice: str = "default"

class TTSResponse(BaseModel):
    audio_url: str
    duration: float
    language: str
    voice: str

# Create TTS directory if it doesn't exist
TTS_DIR = "tts_audio"
os.makedirs(TTS_DIR, exist_ok=True)

def create_dummy_mp3_content() -> bytes:
    """Create a minimal dummy MP3 file content"""
    # This creates a very basic MP3-like header for testing
    # In production, this would be replaced with actual TTS audio
    mp3_header = b'\xff\xfb\x90\x00'  # Basic MP3 frame header
    dummy_audio_data = b'\x00' * 1024  # 1KB of silence
    return mp3_header + dummy_audio_data

def generate_audio_filename(text: str, language: str, voice: str) -> str:
    """Generate consistent filename for audio based on text content"""
    content_hash = hashlib.md5(f"{text}_{language}_{voice}".encode()).hexdigest()[:10]
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"tts_{timestamp}_{content_hash}.mp3"

@router.post("/api/tts/generate", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """Generate TTS audio file"""
    # Generate filename
    filename = generate_audio_filename(request.text, request.language, request.voice)
    file_path = os.path.join(TTS_DIR, filename)
    
    # Create dummy audio file if it doesn't exist
    if not os.path.exists(file_path):
        dummy_content = create_dummy_mp3_content()
        with open(file_path, 'wb') as f:
            f.write(dummy_content)
    
    # Calculate estimated duration (0.6 seconds per word for speech)
    word_count = len(request.text.split())
    estimated_duration = max(1.0, word_count * 0.6)  # Minimum 1 second
    
    audio_url = f"/api/tts/audio/{filename}"
    
    return TTSResponse(
        audio_url=audio_url,
        duration=estimated_duration,
        language=request.language,
        voice=request.voice
    )

@router.get("/api/tts/audio/{filename}")
async def serve_audio(filename: str):
    """Serve TTS audio files"""
    file_path = os.path.join(TTS_DIR, filename)
    
    # If file doesn't exist, create a dummy one
    if not os.path.exists(file_path):
        dummy_content = create_dummy_mp3_content()
        with open(file_path, 'wb') as f:
            f.write(dummy_content)
    
    # Serve the audio file
    return FileResponse(
        file_path, 
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            "Accept-Ranges": "bytes"
        }
    )

@router.get("/api/tts/stream/{filename}")
async def stream_audio(filename: str):
    """Stream audio file (alternative endpoint for streaming)"""
    file_path = os.path.join(TTS_DIR, filename)
    
    if not os.path.exists(file_path):
        dummy_content = create_dummy_mp3_content()
        return StreamingResponse(
            io.BytesIO(dummy_content), 
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "public, max-age=3600"
            }
        )
    
    def file_streamer():
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):  # Read in 8KB chunks
                yield chunk
    
    return StreamingResponse(
        file_streamer(), 
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f"inline; filename={filename}",
            "Cache-Control": "public, max-age=3600"
        }
    )

@router.get("/api/tts/test")
async def test_tts_system():
    """Test endpoint to verify TTS system is working"""
    test_audio_url = "/api/tts/audio/test_sample.mp3"
    
    # Create a test audio file
    test_file_path = os.path.join(TTS_DIR, "test_sample.mp3")
    if not os.path.exists(test_file_path):
        dummy_content = create_dummy_mp3_content()
        with open(test_file_path, 'wb') as f:
            f.write(dummy_content)
    
    return {
        "status": "TTS system operational",
        "test_audio_url": test_audio_url,
        "sample_text": "Hello! This is a test of the TTS system.",
        "instructions": "Use the audio URL to test playback in your frontend"
    }

@router.get("/api/tts/voices")
async def get_available_voices():
    """Get list of available TTS voices"""
    voices = {
        "en": [
            {"id": "en-us-standard", "name": "English (US) - Standard", "gender": "neutral", "sample_url": "/api/tts/audio/sample_en_standard.mp3"},
            {"id": "en-us-female", "name": "English (US) - Female", "gender": "female", "sample_url": "/api/tts/audio/sample_en_female.mp3"},
            {"id": "en-us-male", "name": "English (US) - Male", "gender": "male", "sample_url": "/api/tts/audio/sample_en_male.mp3"},
        ],
        "hi": [
            {"id": "hi-in-standard", "name": "Hindi (India) - Standard", "gender": "neutral", "sample_url": "/api/tts/audio/sample_hi_standard.mp3"},
            {"id": "hi-in-female", "name": "Hindi (India) - Female", "gender": "female", "sample_url": "/api/tts/audio/sample_hi_female.mp3"},
        ],
        "ta": [
            {"id": "ta-in-standard", "name": "Tamil (India) - Standard", "gender": "neutral", "sample_url": "/api/tts/audio/sample_ta_standard.mp3"},
        ]
    }
    
    return {"voices": voices, "note": "All sample URLs return placeholder audio for testing"}

@router.post("/api/tts/batch")
async def generate_batch_tts(texts: list[str], language: str = "en", voice: str = "default"):
    """Generate TTS for multiple texts (useful for pre-generating common responses)"""
    results = []
    
    for text in texts:
        filename = generate_audio_filename(text, language, voice)
        file_path = os.path.join(TTS_DIR, filename)
        
        # Create audio file if it doesn't exist
        if not os.path.exists(file_path):
            dummy_content = create_dummy_mp3_content()
            with open(file_path, 'wb') as f:
                f.write(dummy_content)
        
        word_count = len(text.split())
        duration = max(1.0, word_count * 0.6)
        
        results.append({
            "text": text,
            "audio_url": f"/api/tts/audio/{filename}",
            "duration": duration,
            "language": language,
            "voice": voice
        })
    
    return {"results": results, "total_generated": len(results)}

@router.delete("/api/tts/cleanup")
async def cleanup_old_audio():
    """Clean up old TTS audio files"""
    if not os.path.exists(TTS_DIR):
        return {"message": "No audio directory found"}
    
    files_deleted = 0
    current_time = datetime.now().timestamp()
    
    for filename in os.listdir(TTS_DIR):
        if filename.startswith('test_') or filename.startswith('sample_'):
            continue  # Keep test and sample files
            
        file_path = os.path.join(TTS_DIR, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getctime(file_path)
            # Delete files older than 24 hours (86400 seconds)
            if file_age > 86400:
                os.remove(file_path)
                files_deleted += 1
    
    return {"message": f"Cleaned up {files_deleted} old audio files", "kept_test_files": True}

@router.get("/api/tts/stats")
async def get_media_stats():
    """Get media storage statistics"""
    if not os.path.exists(TTS_DIR):
        return {"total_files": 0, "total_size_mb": 0, "directory_exists": False}
    
    total_files = 0
    total_size = 0
    file_types = {"test": 0, "sample": 0, "generated": 0}
    
    for filename in os.listdir(TTS_DIR):
        file_path = os.path.join(TTS_DIR, filename)
        if os.path.isfile(file_path):
            total_files += 1
            total_size += os.path.getsize(file_path)
            
            # Categorize files
            if filename.startswith('test_'):
                file_types["test"] += 1
            elif filename.startswith('sample_'):
                file_types["sample"] += 1
            else:
                file_types["generated"] += 1
    
    return {
        "total_files": total_files,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "file_types": file_types,
        "directory_path": TTS_DIR,
        "directory_exists": True
    }

@router.get("/api/tts/health")
async def tts_health_check():
    """Health check for TTS system"""
    directory_ok = os.path.exists(TTS_DIR)
    
    # Test file creation
    test_file_path = os.path.join(TTS_DIR, "health_check.mp3")
    write_ok = False
    try:
        dummy_content = create_dummy_mp3_content()
        with open(test_file_path, 'wb') as f:
            f.write(dummy_content)
        write_ok = True
        # Clean up test file
        os.remove(test_file_path)
    except Exception as e:
        write_ok = False
    
    return {
        "status": "healthy" if (directory_ok and write_ok) else "unhealthy",
        "directory_accessible": directory_ok,
        "file_write_ok": write_ok,
        "tts_directory": TTS_DIR,
        "supported_formats": ["mp3"],
        "supported_languages": ["en", "hi", "ta"]
    }
