# Manny Campus Chatbot Backend - API Documentation

## 🚀 Overview
The Manny Campus Chatbot backend is a comprehensive FastAPI application designed to serve as a pre-AI integration system for campus assistance. It provides realistic dummy responses, multi-user thread management, and TTS capabilities.

## 📋 Quick Start

### 1. Start the Server
```bash
cd d:\Coding\SIH25\backend
.\.venv\Scripts\activate
python run_server.py
```
Server runs at: `http://localhost:8000`

### 2. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test Frontend
Open `d:\Coding\SIH25\test_frontend.html` in a browser for interactive testing.

## 🔗 API Endpoints

### Health & Info
- **GET** `/ping` - Health check
- **GET** `/` - Root information

### 💬 Chat API

#### Send Message
**POST** `/api/chat`

**Request Body:**
```json
{
  "user_id": "string",
  "message": "string",
  "language": "en",
  "conversation_id": "string (optional)"
}
```

**Response:**
```json
{
  "response": "AI response text",
  "conversation_id": "unique_thread_id",
  "sources": [
    {
      "title": "Document Title",
      "url": "https://example.com/doc.pdf",
      "snippet": "Relevant excerpt"
    }
  ],
  "language": "en",
  "flags": {
    "contains_personal_info": false,
    "requires_followup": false,
    "confidence_score": 0.85,
    "category": "library",
    "language_detected": "en",
    "sentiment": "neutral",
    "response_type": "informational",
    "urgency_level": "normal",
    "topic_continuation": false,
    "contains_numbers": true,
    "actionable": false
  },
  "tts_audio_url": "/api/tts/audio/response_xxxxx_en.mp3"
}
```

### 🧵 Thread Management

#### Create Thread
**POST** `/api/threads`
```json
{
  "user_id": "string",
  "title": "string"
}
```

#### Get User Threads
**GET** `/api/threads/{user_id}`

Response includes thread list with message counts and timestamps.

#### Get Thread Messages
**GET** `/api/threads/{conversation_id}/messages`

Returns complete message history for a specific thread.

### 🔊 Text-to-Speech

#### Generate TTS
**POST** `/api/tts/generate`
```json
{
  "text": "Text to convert to speech",
  "language": "en",
  "voice": "en-us-female"
}
```

#### Get Available Voices
**GET** `/api/tts/voices`

#### TTS Health Check
**GET** `/api/tts/health`

#### Test Audio
**GET** `/api/tts/test`

#### Batch TTS Generation
**POST** `/api/tts/batch`
```json
["Text 1", "Text 2", "Text 3"]
```

#### TTS Statistics
**GET** `/api/tts/stats`

### 🔐 Authentication

#### Demo Users
**GET** `/auth/demo-users`

#### Login
**POST** `/auth/login`
```json
{
  "user_id": "student123",
  "password": "demo123"
}
```

#### User Profile
**GET** `/auth/profile`
Requires: `Authorization: Bearer <token>` header

## 🎯 Dummy AI Service Features

### Supported Categories
1. **📚 Library** - Hours, study rooms, resources
2. **🍽️ Cafeteria** - Menus, timings, vendors
3. **🎓 Admission** - Requirements, procedures, cutoffs
4. **🏠 Hostel** - Facilities, allocation, rules
5. **💰 Fees** - Structure, payment, scholarships
6. **🚌 Transport** - Routes, schedules, passes
7. **💼 Placement** - Companies, preparation, stats
8. **📖 Academic** - Schedules, exams, attendance

### Response Variations
- Each category has 6+ unique response variations
- Context-aware follow-up detection
- Realistic confidence scoring
- Proper source attribution with PDF links

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy setup
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── thread.py        # Thread model
│   │   └── message.py       # Message model
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── dummy_ai.py      # AI simulation service
│   └── routes/              # API endpoints
│       ├── __init__.py
│       ├── chat.py          # Chat endpoints
│       ├── threads.py       # Thread management
│       ├── tts.py           # Text-to-speech
│       └── auth.py          # Authentication
├── requirements.txt         # Dependencies
├── run_server.py           # Server startup script
└── manny_chatbot.db        # SQLite database
```

## 🧪 Testing

### Automated Testing
Run the comprehensive test suite:
```bash
python test_api_comprehensive.py
```

### Manual Testing
1. **Frontend Interface**: Open `test_frontend.html`
2. **Swagger UI**: http://localhost:8000/docs
3. **Postman**: Import API endpoints from Swagger

### Test Scenarios
- ✅ Multi-user thread isolation
- ✅ Context-aware dummy responses
- ✅ TTS audio generation and serving
- ✅ Authentication with JWT tokens
- ✅ Source attribution for responses
- ✅ Error handling and validation

## 🔧 Configuration

### Environment Variables
- **DATABASE_URL**: SQLite database path (default: `sqlite:///./manny_chatbot.db`)
- **TTS_DIRECTORY**: Audio files storage (default: `tts_audio`)
- **DEBUG**: Enable debug mode (default: `True`)

### Customization Points
1. **Dummy Responses**: Edit `app/services/dummy_ai.py`
2. **Database Models**: Modify `app/models/`
3. **API Routes**: Extend `app/routes/`
4. **Authentication**: Customize `app/routes/auth.py`

## 🚀 Production Readiness

### Current Status: Development/Testing
- ✅ Complete API structure
- ✅ Realistic dummy data
- ✅ Multi-user support
- ✅ TTS integration
- ✅ Authentication framework
- ⚠️ Ready for AI/ML model integration

### Next Steps for Production
1. **AI Integration**: Replace dummy AI service with actual ML models
2. **Database**: Migrate from SQLite to PostgreSQL/MySQL
3. **Authentication**: Implement proper user registration and OAuth
4. **TTS**: Integrate with real TTS services (Google Cloud TTS, Azure Cognitive Services)
5. **Caching**: Add Redis for session management
6. **Monitoring**: Add logging and metrics collection

## 📱 Frontend Integration

### JSON Contract
The API provides consistent JSON responses matching the final AI contract:
- `response`: Main AI response text
- `conversation_id`: Unique thread identifier
- `sources`: Array of source documents
- `language`: Detected/specified language
- `flags`: Metadata about the response
- `tts_audio_url`: Audio file URL for TTS

### CORS Configuration
CORS is enabled for all origins in development. Update for production security.

### Error Handling
- HTTP 422: Validation errors
- HTTP 404: Resource not found
- HTTP 500: Server errors

## 📞 Support

For issues or questions:
1. Check the comprehensive test output
2. Review Swagger documentation at `/docs`
3. Examine the test frontend implementation
4. Verify server logs in the terminal

## 🏆 Features Completed

✅ **FastAPI Backend**: Complete REST API with auto-documentation  
✅ **Dummy AI Service**: 8 categories, 6+ variations each, context awareness  
✅ **Multi-User Threads**: User isolation, message history, thread management  
✅ **TTS System**: Audio generation, multiple voices, file serving  
✅ **Authentication**: JWT-like tokens, demo users, profile management  
✅ **Database Integration**: SQLAlchemy ORM, automatic schema creation  
✅ **CORS Support**: Frontend integration ready  
✅ **Error Handling**: Comprehensive validation and error responses  
✅ **Testing  Suite**: Automated tests and frontend demo  
✅ **Documentation**: Swagger UI, ReDoc, comprehensive API docs  

The backend is **100% ready** for frontend integration and can seamlessly transition to real AI models when available! 🎯
