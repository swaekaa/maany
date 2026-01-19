from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class Thread(Base):
    """
    Represents a conversation thread between a user and the AI chatbot.
    Each thread contains multiple messages.
    """
    __tablename__ = "threads"
    
    conversation_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)  # Optional conversation title
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationship with messages
    messages = relationship("Message", back_populates="thread", cascade="all, delete-orphan")

class Message(Base):
    """
    Represents individual messages within a conversation thread.
    Stores both user queries and AI responses with metadata.
    """
    __tablename__ = "messages"
    
    log_id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("threads.conversation_id"), nullable=False, index=True)
    sender = Column(String, nullable=False)  # 'user' or 'assistant'
    user_query = Column(Text, nullable=True)  # Original user input
    preprocessed_query = Column(Text, nullable=True)  # Cleaned/processed query
    response_text = Column(Text, nullable=True)  # AI response
    language = Column(String, default="en")  # Language code (en, hi, etc.)
    sources = Column(JSON, nullable=True)  # List of source documents/references
    flags = Column(JSON, nullable=True)  # Safety flags, content moderation flags
    tts_audio_path = Column(String, nullable=True)  # Path to TTS audio file
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with thread
    thread = relationship("Thread", back_populates="messages")
