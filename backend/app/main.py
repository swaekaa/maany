from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.database import create_tables
from app.routes import chat, threads, tts, auth

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Manny Campus Chatbot - SIH 2025 Project"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is starting up!")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🎯 Environment: {'Development' if settings.DEBUG else 'Production'}")

# Include routers
app.include_router(chat.router)
app.include_router(threads.router)
app.include_router(tts.router)
app.include_router(auth.router)

# Health check endpoint
@app.get("/ping")
async def ping():
    """Health check endpoint to verify the API is running."""
    return {
        "status": "ok",
        "message": "Manny Campus Chatbot API is running!",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Backend API for Manny Campus Chatbot",
        "docs_url": "/docs",
        "health_check": "/ping",
        "chat_endpoint": "/api/chat",
        "message": "Welcome to Manny Campus Chatbot API! 🤖"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
