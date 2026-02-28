import os
from typing import Optional

class Settings:
    # Application
    APP_NAME: str = "Manny Campus Chatbot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./manny_chatbot.db"
    
    # AI/ML Integration (for future use)
    AI_MODEL_ENDPOINT: Optional[str] = None
    AI_API_KEY: Optional[str] = None
    
    # TTS (Text-to-Speech) Settings
    TTS_OUTPUT_DIR: str = "./tts"
    
    # Security
    SECRET_KEY: str = "your-secret-key-for-hackathon"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]  # In production, specify actual frontend URLs
    
    # Logging
    LOG_LEVEL: str = "INFO"

# Create settings instance
settings = Settings()

# Ensure TTS directory exists
os.makedirs(settings.TTS_OUTPUT_DIR, exist_ok=True)
