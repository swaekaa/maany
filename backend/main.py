from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, List

from database import get_db, engine
from models import Base, Message
from schemas import ChatMessage, ChatResponse, ResourceResponse, MessageResponse, StudentChatHistory
from crud import create_message, get_messages, get_messages_by_student

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Manny Backend API", 
    version="1.0.0",
    description="Backend API for Manny - Multilingual Campus Chatbot",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration - very permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8001")

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Manny Backend API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "ai_api": "configured" if AI_API_URL else "not_configured"
        }
    }

@app.post("/chat/message", response_model=ChatResponse, tags=["Chat"])
async def send_message(message_data: ChatMessage, db: Session = Depends(get_db)):
    """
    Handle chat messages from students.
    
    This endpoint:
    1. Logs the student message to database
    2. Forwards the message to AI service
    3. Logs the AI response to database  
    4. Returns the response to frontend
    
    Perfect for any frontend framework to integrate with.
    """
    try:
        # Log student message
        student_message = create_message(
            db=db,
            student_id=message_data.student_id,
            role="student",
            content=message_data.message
        )
        
        # Forward to AI API
        bot_reply = ""
        resources = []
        
        try:
            async with httpx.AsyncClient() as client:
                ai_response = await client.post(
                    f"{AI_API_URL}/process",
                    json={
                        "message": message_data.message, 
                        "student_id": message_data.student_id,
                        "context": "campus_assistant"
                    },
                    timeout=30.0
                )
                if ai_response.status_code == 200:
                    ai_data = ai_response.json()
                    bot_reply = ai_data.get("reply", "I'm still learning. Please try again later.")
                    resources = ai_data.get("resources", [])
                else:
                    bot_reply = "Sorry, I'm having trouble processing your request right now."
        except Exception as ai_error:
            # Fallback response when AI API is not available
            print(f"AI API Error: {ai_error}")
            bot_reply = f"Hello! I received your message: '{message_data.message}'. The AI service is being set up by the team. For now, I can help you with basic campus information!"
        
        # Log bot response
        bot_message = create_message(
            db=db,
            student_id=message_data.student_id,
            role="bot",
            content=bot_reply
        )
        
        return ChatResponse(
            reply=bot_reply, 
            resources=resources,
            message_id=bot_message.id,
            timestamp=bot_message.timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/chat/history/{student_id}", response_model=StudentChatHistory, tags=["Chat"])
async def get_student_chat_history(
    student_id: str, 
    limit: int = Query(50, description="Number of messages to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get chat history for a specific student.
    Useful for frontend to restore conversation when student returns.
    """
    messages = get_messages_by_student(db, student_id)
    # Limit messages and convert to response format
    recent_messages = messages[-limit:] if len(messages) > limit else messages
    
    message_responses = [
        MessageResponse(
            id=msg.id,
            student_id=msg.student_id,
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp
        ) for msg in recent_messages
    ]
    
    return StudentChatHistory(
        student_id=student_id,
        messages=message_responses,
        total_messages=len(messages)
    )

@app.get("/resources/{resource_type}", response_model=ResourceResponse, tags=["Resources"])
async def get_resources(resource_type: str):
    """
    Get campus resources (timetable, syllabus, notices).
    
    Frontend can call this to get structured campus data.
    Currently returns dummy data - replace with real SLCM integration.
    """
    dummy_data = {
        "timetable": {
            "type": "timetable",
            "data": {
                "Monday": [
                    {"time": "9:00 AM", "subject": "Mathematics", "room": "A101", "faculty": "Dr. Smith"},
                    {"time": "11:00 AM", "subject": "Physics", "room": "B205", "faculty": "Prof. Johnson"},
                    {"time": "2:00 PM", "subject": "Chemistry", "room": "C301", "faculty": "Dr. Brown"}
                ],
                "Tuesday": [
                    {"time": "10:00 AM", "subject": "English", "room": "A102", "faculty": "Ms. Davis"},
                    {"time": "1:00 PM", "subject": "Computer Science", "room": "D401", "faculty": "Dr. Wilson"}
                ],
                "Wednesday": [
                    {"time": "9:00 AM", "subject": "Mathematics", "room": "A101", "faculty": "Dr. Smith"},
                    {"time": "3:00 PM", "subject": "Lab Session", "room": "L501", "faculty": "Lab Assistant"}
                ]
            }
        },
        "syllabus": {
            "type": "syllabus",
            "data": {
                "subjects": [
                    {
                        "name": "Mathematics",
                        "code": "MATH101",
                        "topics": ["Calculus", "Linear Algebra", "Statistics"],
                        "credits": 4,
                        "books": ["Advanced Mathematics by XYZ"]
                    },
                    {
                        "name": "Physics", 
                        "code": "PHY101",
                        "topics": ["Mechanics", "Thermodynamics", "Optics"],
                        "credits": 4,
                        "books": ["Fundamentals of Physics by ABC"]
                    },
                    {
                        "name": "Computer Science",
                        "code": "CS101", 
                        "topics": ["Data Structures", "Algorithms", "Database Systems"],
                        "credits": 3,
                        "books": ["Introduction to Algorithms by DEF"]
                    }
                ]
            }
        },
        "notices": {
            "type": "notices",
            "data": [
                {
                    "id": 1,
                    "title": "Mid-term Exams",
                    "date": "2025-09-15",
                    "content": "Mid-term examinations will start from September 15th. Please check your exam schedule.",
                    "priority": "high",
                    "category": "academic"
                },
                {
                    "id": 2,
                    "title": "Library Hours Extended",
                    "date": "2025-09-10",
                    "content": "Library will remain open until 10 PM during exam period.",
                    "priority": "medium",
                    "category": "facility"
                },
                {
                    "id": 3,
                    "title": "Cultural Fest",
                    "date": "2025-09-20",
                    "content": "Annual cultural festival will be held on September 20th. Registration open!",
                    "priority": "low",
                    "category": "event"
                }
            ]
        },
        "attendance": {
            "type": "attendance",
            "data": {
                "overall_percentage": 85.5,
                "subjects": [
                    {"name": "Mathematics", "attended": 42, "total": 48, "percentage": 87.5},
                    {"name": "Physics", "attended": 38, "total": 45, "percentage": 84.4},
                    {"name": "Computer Science", "attended": 40, "total": 46, "percentage": 87.0}
                ],
                "last_updated": "2025-09-04"
            }
        }
    }
    
    if resource_type not in dummy_data:
        available_types = list(dummy_data.keys())
        raise HTTPException(
            status_code=404, 
            detail=f"Resource type '{resource_type}' not found. Available types: {available_types}"
        )
    
    return ResourceResponse(**dummy_data[resource_type])

@app.get("/resources", tags=["Resources"])
async def list_available_resources():
    """
    List all available resource types.
    Helpful for frontend to know what resources can be fetched.
    """
    return {
        "available_resources": [
            {"type": "timetable", "description": "Class schedule and timing"},
            {"type": "syllabus", "description": "Course syllabus and curriculum"},
            {"type": "notices", "description": "Official announcements and notices"},
            {"type": "attendance", "description": "Student attendance records"}
        ]
    }

@app.get("/admin/logs", tags=["Admin"])
async def get_chat_logs(
    limit: int = Query(100, description="Number of messages to retrieve"),
    student_id: Optional[str] = Query(None, description="Filter by specific student"),
    db: Session = Depends(get_db)
):
    """
    Get conversation logs for admin review.
    Can filter by student_id or get all conversations.
    """
    if student_id:
        messages = get_messages_by_student(db, student_id)
    else:
        messages = get_messages(db, limit=limit)
    
    return {
        "logs": [
            MessageResponse(
                id=msg.id,
                student_id=msg.student_id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp
            ) for msg in messages
        ],
        "total_messages": len(messages),
        "filtered_by": student_id if student_id else "all_students"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
