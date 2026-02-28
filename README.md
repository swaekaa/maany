# Manny Backend - Multilingual Campus Chatbot API

## 🎯 Project Overview

**Manny Backend** provides a robust REST API for a multilingual campus chatbot that integrates with SLCM portals. The backend handles chat messaging, campus resource retrieval, conversation logging, and seamless integration with AI services.

## 🚀 Quick Start

### Method 1: Using Startup Scripts
```bash
# Windows
cd backend
start.bat

# Linux/Mac  
cd backend
chmod +x start.sh
./start.sh
```

### Method 2: Manual Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env  # Edit with your settings
python main.py
```

**Server runs on:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Detailed health status |
| `POST` | `/chat/message` | Send chat message |
| `GET` | `/chat/history/{student_id}` | Get student chat history |
| `GET` | `/resources` | List available resource types |
| `GET` | `/resources/{type}` | Get specific campus resource |
| `GET` | `/admin/logs` | Get conversation logs (admin) |

## 🔌 Frontend Integration

### Simple Example (Any Framework)
```javascript
// Send message
const response = await fetch('http://localhost:8000/chat/message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    student_id: 'STU123456',
    message: 'What is my timetable?'
  })
});

const data = await response.json();
console.log('Reply:', data.reply);
console.log('Resources:', data.resources);
```

### Get Resources
```javascript
// Get timetable
const timetable = await fetch('http://localhost:8000/resources/timetable');
const data = await timetable.json();

// Available types: timetable, syllabus, notices, attendance
```

## 🤖 AI Team Integration

Your AI team just needs to provide an API endpoint that accepts:

**Request:**
```json
POST {AI_API_URL}/process
{
  "message": "student question",
  "student_id": "STU123456",
  "context": "campus_assistant"
}
```

**Expected Response:**
```json
{
  "reply": "AI response text",
  "resources": [
    {"type": "timetable", "title": "Schedule", "data": {...}}
  ]
}
```

Set `AI_API_URL` in your `.env` file and the backend handles the rest!

## 📊 Features

✅ **Complete REST API** - All endpoints documented with OpenAPI  
✅ **Database Integration** - SQLite (dev) / PostgreSQL (prod)  
✅ **Chat History** - Full conversation logging per student  
✅ **Campus Resources** - Timetable, syllabus, notices, attendance  
✅ **AI Integration Ready** - Forwards to your AI service  
✅ **CORS Enabled** - Works with any frontend framework  
✅ **Health Monitoring** - Built-in health check endpoints  
✅ **Admin Panel** - Conversation logs and analytics  

## 🛠 Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM  
- **PostgreSQL/SQLite** - Database
- **Pydantic** - Data validation
- **HTTPX** - Async HTTP client for AI integration
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application & routes
├── database.py          # Database configuration  
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── start.bat           # Windows startup script
├── start.sh            # Linux/Mac startup script
└── API_DOCS.md         # Detailed API documentation
```

## 🔧 Configuration

Edit `.env` file:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/manny_db
AI_API_URL=http://localhost:8001
SECRET_KEY=your-secret-key
DEBUG=True
```

## 🚀 Deployment Ready

- **Docker**: Ready for containerization
- **Environment Variables**: All config externalized  
- **Health Checks**: Built-in monitoring endpoints
- **CORS**: Configurable for production
- **Database**: Supports both SQLite and PostgreSQL

## 👥 Team Integration

**Frontend Team:** Use any framework (React, Vue, Angular, plain JS) - just call the REST API  
**AI Team:** Provide your API endpoint - backend forwards all chat messages  
**DevOps Team:** Standard FastAPI deployment with health checks  

**Perfect for hackathon speed! 🏆**
