from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    student_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    resources: Optional[List[Dict[str, Any]]] = []
    message_id: Optional[int] = None
    timestamp: Optional[datetime] = None

class ResourceResponse(BaseModel):
    type: str
    data: Dict[str, Any]

class MessageResponse(BaseModel):
    id: int
    student_id: str
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class StudentChatHistory(BaseModel):
    student_id: str
    messages: List[MessageResponse]
    total_messages: int

class ApiResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
