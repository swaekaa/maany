from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from app.models.database import get_db
from app.models.models import Thread, Message
from app.core.config import settings
from app.services.dummy_ai import DummyAIService

router = APIRouter(prefix="/api", tags=["chat"])
dummy_ai = DummyAIService()

# Pydantic models for API
class ChatRequest(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    message: str
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[Dict[str, str]]
    language: str
    flags: Dict[str, Any]
    tts_audio_url: Optional[str] = None

class ThreadResponse(BaseModel):
    conversation_id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int

class MessageResponse(BaseModel):
    log_id: str
    conversation_id: str
    sender: str
    user_query: Optional[str]
    response_text: Optional[str]
    language: str
    timestamp: datetime

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint that processes user messages and returns AI responses.
    Creates conversation threads and logs all interactions.
    """
    
    # Generate conversation_id if not provided
    conversation_id = request.conversation_id or f"user_{request.user_id}_session_{uuid.uuid4().hex[:8]}"
    
    # Check if thread exists, create if not
    thread = db.query(Thread).filter(Thread.conversation_id == conversation_id).first()
    if not thread:
        thread = Thread(
            conversation_id=conversation_id,
            user_id=request.user_id,
            title=f"Chat Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(thread)
        db.commit()
    
    # Generate unique log ID
    log_id = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    # Log user message
    preprocessed_query = request.message.lower().strip()
    user_message = Message(
        log_id=f"{log_id}_user",
        conversation_id=conversation_id,
        sender="user",
        user_query=request.message,
        preprocessed_query=preprocessed_query,
        language=request.language or "en",
        flags={"type": "user_input", "safe": True}
    )
    db.add(user_message)
    
    # Get conversation history for context
    conversation_history = []
    if conversation_id:
        existing_messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
        conversation_history = [{"user_query": msg.user_query, "response_text": msg.response_text} for msg in existing_messages[-5:]]  # Last 5 messages
    
    # Generate AI response using dummy AI service
    ai_response = dummy_ai.generate_response(
        query=request.message,
        language=request.language or "en",
        conversation_history=conversation_history
    )
    
    # Generate TTS path (simulated)
    tts_path = ai_response.get("tts_audio_url", f"{settings.TTS_OUTPUT_DIR}/{conversation_id}_response_{uuid.uuid4().hex[:6]}.mp3")
    
    # Log AI response
    ai_message = Message(
        log_id=f"{log_id}_ai",
        conversation_id=conversation_id,
        sender="assistant",
        user_query=request.message,
        preprocessed_query=preprocessed_query,
        response_text=ai_response["response"],
        language=request.language or "en",
        sources=ai_response["sources"],
        flags=ai_response["flags"],
        tts_audio_path=tts_path
    )
    db.add(ai_message)
    db.commit()
    
    # Return response
    return ChatResponse(
        response=ai_response["response"],
        conversation_id=conversation_id,
        sources=ai_response["sources"],
        language=request.language or "en",
        flags=ai_response["flags"],
        tts_audio_url=ai_response.get("tts_audio_url")
    )

@router.get("/threads/{user_id}", response_model=List[ThreadResponse])
async def get_user_threads(user_id: str, db: Session = Depends(get_db)):
    """Get all conversation threads for a specific user."""
    threads = db.query(Thread).filter(Thread.user_id == user_id).all()
    
    result = []
    for thread in threads:
        message_count = db.query(Message).filter(Message.conversation_id == thread.conversation_id).count()
        result.append(ThreadResponse(
            conversation_id=thread.conversation_id,
            user_id=thread.user_id,
            title=thread.title,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
            message_count=message_count
        ))
    
    return result

@router.get("/thread/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_thread_messages(conversation_id: str, db: Session = Depends(get_db)):
    """Get all messages in a specific conversation thread."""
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    
    return [MessageResponse(
        log_id=msg.log_id,
        conversation_id=msg.conversation_id,
        sender=msg.sender,
        user_query=msg.user_query,
        response_text=msg.response_text,
        language=msg.language,
        timestamp=msg.timestamp
    ) for msg in messages]

def generate_sample_response(user_query: str, preprocessed_query: str) -> Dict[str, Any]:
    """
    Generate sample AI responses for demonstration.
    In production, this would be replaced with actual AI/ML model calls.
    """
    
    query_lower = preprocessed_query.lower()
    
    # Sample responses based on common campus queries
    if any(word in query_lower for word in ["form", "submit", "submission"]):
        return {
            "response_text": "You can submit the form at the academic office on the 2nd floor before 5 PM. Make sure to bring all required documents.",
            "sources": ["academic_rules.pdf#page3", "syllabus.pdf#page2"],
            "flags": {"safe": True, "inappropriate": False, "confidence": 0.95},
            "safe_to_respond": True
        }
    
    elif any(word in query_lower for word in ["library", "book", "borrow"]):
        return {
            "response_text": "The library is open from 8 AM to 8 PM on weekdays. You can search for books online and reserve them through the library portal.",
            "sources": ["library_guide.pdf#page1", "student_handbook.pdf#page15"],
            "flags": {"safe": True, "inappropriate": False, "confidence": 0.92},
            "safe_to_respond": True
        }
    
    elif any(word in query_lower for word in ["exam", "test", "schedule"]):
        return {
            "response_text": "Exam schedules are published 2 weeks before the exam period. Check your student portal for the latest updates and venue details.",
            "sources": ["exam_guidelines.pdf#page1", "academic_calendar.pdf#page3"],
            "flags": {"safe": True, "inappropriate": False, "confidence": 0.88},
            "safe_to_respond": True
        }
    
    elif any(word in query_lower for word in ["fee", "payment", "dues"]):
        return {
            "response_text": "Fee payments can be made online through the student portal or at the accounts office. The deadline for this semester is mentioned in your fee receipt.",
            "sources": ["fee_structure.pdf#page2", "payment_guidelines.pdf#page1"],
            "flags": {"safe": True, "inappropriate": False, "confidence": 0.90},
            "safe_to_respond": True
        }
    
    else:
        return {
            "response_text": f"I understand you're asking about '{user_query}'. I'm here to help with campus-related queries. Could you please provide more specific details?",
            "sources": ["general_help.pdf#page1"],
            "flags": {"safe": True, "inappropriate": False, "confidence": 0.70},
            "safe_to_respond": True
        }
