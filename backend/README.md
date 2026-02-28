# Manny Campus Chatbot - Backend API

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env file with your configurations
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API:** `http://localhost:8000`
- **Documentation:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/ping`

## 📡 API Endpoints

### Health Check
- `GET /ping` - Health check endpoint
- `GET /` - Root endpoint with API info

### Chat Endpoints
- `POST /api/chat` - Main chat endpoint
- `GET /api/threads/{user_id}` - Get user's conversation threads
- `GET /api/thread/{conversation_id}/messages` - Get messages in a thread

## 🗄️ Database Schema

### Thread Table
- `conversation_id` (Primary Key)
- `user_id`
- `title`
- `created_at`, `updated_at`
- `is_active`

### Message Table
- `log_id` (Primary Key)
- `conversation_id` (Foreign Key)
- `sender` (user/assistant)
- `user_query`
- `preprocessed_query`
- `response_text`
- `language`
- `sources` (JSON)
- `flags` (JSON)
- `tts_audio_path`
- `timestamp`

## 🤖 Sample API Usage

### Send Chat Message
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_12345",
    "message": "Where can I submit my form?",
    "language": "en"
  }'
```

### Get User Threads
```bash
curl "http://localhost:8000/api/threads/student_12345"
```

## 🔧 Project Structure

```
backend/
├── app/
│   ├── main.py             # FastAPI entrypoint
│   ├── core/
│   │   └── config.py       # Settings and constants
│   ├── models/
│   │   ├── database.py     # DB connection setup
│   │   └── models.py       # SQLAlchemy models
│   └── routes/
│       └── chat.py         # Chat API routes
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🎯 Features

✅ **SQLite Database** with conversation logging  
✅ **Thread Management** for organizing conversations  
✅ **Message Logging** with metadata (sources, flags, TTS paths)  
✅ **Sample AI Responses** for testing  
✅ **CORS Support** for frontend integration  
✅ **Auto Documentation** via FastAPI  
✅ **Health Monitoring** endpoints  

## 🔄 Next Steps

1. **AI Integration:** Replace sample responses with actual ML model calls
2. **Authentication:** Add user authentication middleware
3. **File Upload:** Support for document/image uploads
4. **TTS Integration:** Implement actual text-to-speech generation
5. **Caching:** Add Redis for response caching
6. **Monitoring:** Add logging and metrics collection

## 🚀 Ready for Hackathon!

The backend is fully functional and ready to integrate with:
- Frontend React application
- AI/ML models
- Authentication systems
- File storage services
