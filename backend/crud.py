from sqlalchemy.orm import Session
from models import Message
from schemas import MessageResponse
from typing import List

def create_message(db: Session, student_id: str, role: str, content: str) -> Message:
    """Create a new message in the database"""
    db_message = Message(
        student_id=student_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, skip: int = 0, limit: int = 100) -> List[Message]:
    """Get messages from the database"""
    return db.query(Message).offset(skip).limit(limit).all()

def get_messages_by_student(db: Session, student_id: str) -> List[Message]:
    """Get all messages for a specific student"""
    return db.query(Message).filter(Message.student_id == student_id).all()
