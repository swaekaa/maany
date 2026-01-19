"""
Thread management endpoints for conversation handling
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models.database import get_db
from ..models.models import Thread, Message
from ..services.dummy_ai import DummyAIService
from pydantic import BaseModel

router = APIRouter()
dummy_ai = DummyAIService()

class ThreadResponse(BaseModel):
    conversation_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int
    last_message_preview: str

class CreateThreadRequest(BaseModel):
    user_id: str
    title: str = None

class ThreadListResponse(BaseModel):
    threads: List[ThreadResponse]
    total_count: int

@router.get("/api/threads/{user_id}", response_model=ThreadListResponse)
async def get_user_threads(user_id: str, db: Session = Depends(get_db)):
    """Get all conversation threads for a user"""
    threads = db.query(Thread).filter(Thread.user_id == user_id).order_by(Thread.updated_at.desc()).all()
    
    thread_responses = []
    for thread in threads:
        # Get message count and last message
        messages = db.query(Message).filter(Message.conversation_id == thread.conversation_id).all()
        message_count = len(messages)
        last_message = messages[-1] if messages else None
        
        thread_responses.append(ThreadResponse(
            conversation_id=str(thread.conversation_id),
            title=str(thread.title),
            created_at=thread.created_at,
            updated_at=thread.updated_at,
            message_count=message_count,
            last_message_preview=str(last_message.response_text)[:100] + "..." if last_message and len(str(last_message.response_text)) > 100 else (str(last_message.response_text) if last_message else "")
        ))
    
    return ThreadListResponse(threads=thread_responses, total_count=len(thread_responses))

@router.post("/api/threads", response_model=dict)
async def create_thread(request: CreateThreadRequest, db: Session = Depends(get_db)):
    """Create a new conversation thread"""
    # Generate conversation ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    conversation_id = f"conv_{timestamp}_{request.user_id}_{hash(request.user_id) % 1000:03d}"
    
    # Create thread
    thread = Thread(
        conversation_id=conversation_id,
        user_id=request.user_id,
        title=request.title or f"New Conversation {datetime.now().strftime('%m/%d %H:%M')}",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(thread)
    db.commit()
    db.refresh(thread)
    
    return {
        "conversation_id": conversation_id,
        "message": "Thread created successfully"
    }

@router.get("/api/threads/{conversation_id}/messages")
async def get_thread_messages(conversation_id: str, db: Session = Depends(get_db)):
    """Get all messages in a conversation thread"""
    # Verify thread exists
    thread = db.query(Thread).filter(Thread.conversation_id == conversation_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Get messages
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "log_id": str(msg.log_id),
            "sender": str(msg.sender),
            "user_query": str(msg.user_query),
            "response_text": str(msg.response_text),
            "language": str(msg.language),
            "sources": msg.sources,
            "flags": msg.flags,
            "timestamp": msg.timestamp,
            "tts_audio_path": str(msg.tts_audio_path)
        })
    
    return {
        "conversation_id": conversation_id,
        "thread_title": thread.title,
        "messages": formatted_messages,
        "total_messages": len(formatted_messages)
    }

@router.delete("/api/threads/{conversation_id}")
async def delete_thread(conversation_id: str, db: Session = Depends(get_db)):
    """Delete a conversation thread and all its messages"""
    # Delete messages first
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    
    # Delete thread
    thread = db.query(Thread).filter(Thread.conversation_id == conversation_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    db.delete(thread)
    db.commit()
    
    return {"message": "Thread deleted successfully"}

@router.put("/api/threads/{conversation_id}/title")
async def update_thread_title(conversation_id: str, title: str, db: Session = Depends(get_db)):
    """Update thread title"""
    thread = db.query(Thread).filter(Thread.conversation_id == conversation_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread.title = title
    thread.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Thread title updated successfully"}
