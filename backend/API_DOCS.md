# Manny Backend API Documentation

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
copy .env.example .env
# Edit .env with your database URL and AI API endpoint
```

### 3. Run Server
```bash
python main.py
```

Server runs on: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### **Health & Status**

#### `GET /`
Basic health check
```json
{
  "message": "Manny Backend API is running!",
  "version": "1.0.0", 
  "status": "healthy"
}
```

#### `GET /health`
Detailed health status
```json
{
  "status": "healthy",
  "timestamp": "2025-09-04T10:30:00",
  "services": {
    "database": "connected",
    "ai_api": "configured"
  }
}
```

---

### **Chat Endpoints**

#### `POST /chat/message`
Send a chat message

**Request:**
```json
{
  "student_id": "STU123456",
  "message": "What's my timetable for today?"
}
```

**Response:**
```json
{
  "reply": "Here's your timetable for today...",
  "resources": [
    {
      "type": "timetable",
      "title": "Today's Schedule",
      "data": {...}
    }
  ],
  "message_id": 42,
  "timestamp": "2025-09-04T10:30:00"
}
```

#### `GET /chat/history/{student_id}?limit=50`
Get student's chat history

**Response:**
```json
{
  "student_id": "STU123456",
  "messages": [
    {
      "id": 1,
      "student_id": "STU123456", 
      "role": "student",
      "content": "Hello",
      "timestamp": "2025-09-04T10:00:00"
    },
    {
      "id": 2,
      "student_id": "STU123456",
      "role": "bot", 
      "content": "Hi! How can I help?",
      "timestamp": "2025-09-04T10:00:01"
    }
  ],
  "total_messages": 2
}
```

---

### **Resource Endpoints**

#### `GET /resources`
List available resource types

**Response:**
```json
{
  "available_resources": [
    {"type": "timetable", "description": "Class schedule and timing"},
    {"type": "syllabus", "description": "Course syllabus and curriculum"},
    {"type": "notices", "description": "Official announcements"},
    {"type": "attendance", "description": "Student attendance records"}
  ]
}
```

#### `GET /resources/{resource_type}`
Get specific resource data

**Available types:** `timetable`, `syllabus`, `notices`, `attendance`

**Response Example (timetable):**
```json
{
  "type": "timetable",
  "data": {
    "Monday": [
      {
        "time": "9:00 AM",
        "subject": "Mathematics", 
        "room": "A101",
        "faculty": "Dr. Smith"
      }
    ]
  }
}
```

---

### **Admin Endpoints**

#### `GET /admin/logs?limit=100&student_id=STU123456`
Get chat logs for admin review

**Response:**
```json
{
  "logs": [...],
  "total_messages": 150,
  "filtered_by": "STU123456"
}
```

---

## 🔌 Frontend Integration Guide

### **Simple JavaScript Example**
```javascript
// Send chat message
const response = await fetch('http://localhost:8000/chat/message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    student_id: 'STU123456',
    message: 'What are my upcoming assignments?'
  })
});

const data = await response.json();
console.log('Bot reply:', data.reply);
console.log('Resources:', data.resources);
```

### **Get Student History**
```javascript
const history = await fetch('http://localhost:8000/chat/history/STU123456?limit=20');
const chatData = await history.json();
console.log('Previous messages:', chatData.messages);
```

### **Get Campus Resources**
```javascript
const timetable = await fetch('http://localhost:8000/resources/timetable');
const schedule = await timetable.json();
console.log('Today\'s classes:', schedule.data);
```

---

## 🛠 Integration with AI Team

The backend automatically forwards chat messages to your AI team's API:

**AI API Expected Format:**
```javascript
// Request to AI service
POST {AI_API_URL}/process
{
  "message": "student question",
  "student_id": "STU123456", 
  "context": "campus_assistant"
}

// Expected AI response
{
  "reply": "AI generated response",
  "resources": [
    {
      "type": "timetable",
      "title": "Your Schedule", 
      "data": {...}
    }
  ]
}
```

---

## 🔒 CORS & Security

- **Development:** CORS allows all origins (`*`)
- **Production:** Update `allow_origins` in main.py
- **Authentication:** Ready for SLCM session integration
- **Rate Limiting:** Can be added via middleware

---

## 📊 Database Schema

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR NOT NULL,
    role VARCHAR NOT NULL,  -- 'student' or 'bot'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Deployment Ready

- **Environment Variables:** Configured via `.env`
- **Database:** PostgreSQL for production, SQLite for development
- **Docker:** Ready for containerization
- **Health Checks:** Built-in endpoints for monitoring
- **Logging:** All conversations automatically logged

**Perfect for any frontend framework: React, Vue, Angular, or plain JavaScript!**
