from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from pathlib import Path
import sys
import os

# Add services folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../services"))

from app.models.database import get_db
from app.models.models import Thread, Message
from app.core.config import settings

# Import your RAG + agents
from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent
from RAG1 import rag_query, rg_generate

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize agents once
input_agent = InputPreprocessorAgent()
safety_agent = SafetyFilterAgent()


# Pydantic models
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


@router.get("/threads/{user_id}")
async def get_user_threads(user_id: str, db: Session = Depends(get_db)):
    threads = db.query(Thread).filter(Thread.user_id == user_id).order_by(Thread.created_at.desc()).all()
    return [
        {
            "conversation_id": t.conversation_id,
            "title": t.title,
            "created_at": t.created_at
        }
        for t in threads
    ]
@router.get("/threads/{conversation_id}/messages")
async def get_thread_messages(conversation_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.id.asc()).all()
    return [
        {
            "sender": m.sender,
            "user_query": m.user_query,
            "response_text": m.response_text,
            "language": m.language,
            "sources": m.sources,
            "tts_audio_url": m.tts_audio_path,
            "flags": m.flags,
            "created_at": m.created_at
        }
        for m in messages
    ]
# Chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # 1️⃣ Generate conversation ID if not provided
    conversation_id = request.conversation_id or f"user_{request.user_id}_session_{uuid.uuid4().hex[:8]}"
    
    # 2️⃣ Check/create thread
    thread = db.query(Thread).filter(Thread.conversation_id == conversation_id).first()
    if not thread:
        thread = Thread(
            conversation_id=conversation_id,
            user_id=request.user_id,
            title=f"Chat Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(thread)
        db.commit()
    
    # 3️⃣ Log user message
    log_id = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    user_input_json = {
        "thread_id": thread.conversation_id,
        "user_id": request.user_id,
        "query": request.message
    }
    
    # 4️⃣ Agent 1: Preprocessing
    try:
        processed_input = input_agent.run(user_input_json, use_voice=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in preprocessing: {e}")
    
    # 5️⃣ Agent 2: Safety
    safety_result = safety_agent.run(processed_input)
    if not safety_result["safety"]["safe"]:
        raise HTTPException(status_code=400, detail=f"Blocked by Safety Agent: {safety_result['safety']['reason']}")
    
    # 6️⃣ RAG Retrieval
    rag_output = rag_query(processed_input["query_en"])
    if not rag_output["context"]:
        raise HTTPException(status_code=404, detail="No relevant context found in PDFs.")
    
    # 7️⃣ Response Generation
    response_text, sources = rg_generate(
        user_id=processed_input["user_id"],
        thread_id=processed_input["thread_id"],
        preprocessed_json=safety_result,
        rag_output=rag_output,
        history_turns=5
    )
    
    # 8️⃣ TTS placeholder
    tts_path = f"{settings.TTS_OUTPUT_DIR}/{conversation_id}_response_{uuid.uuid4().hex[:6]}.mp3"
    
    # 9️⃣ Save user message
    user_message = Message(
        log_id=f"{log_id}_user",
        conversation_id=conversation_id,
        sender="user",
        user_query=request.message,
        preprocessed_query=processed_input["query_en"],
        language=request.language or "en",
        flags={"type": "user_input", "safe": True}
    )
    db.add(user_message)
    
    # 10️⃣ Save AI response
    ai_message = Message(
        log_id=f"{log_id}_ai",
        conversation_id=conversation_id,
        sender="assistant",
        user_query=request.message,
        preprocessed_query=processed_input["query_en"],
        response_text=response_text,
        language=request.language or "en",
        sources=sources,
        flags={"safe": True},
        tts_audio_path=tts_path
    )
    db.add(ai_message)
    db.commit()
    
    # 11️⃣ Return API response
    return ChatResponse(
        response=response_text,
        conversation_id=conversation_id,
        sources=sources,
        language=request.language or "en",
        flags={"safe": True},
        tts_audio_url=tts_path
    )
