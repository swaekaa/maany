"""
User authentication and session management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import secrets

from ..models.database import get_db

router = APIRouter()
security = HTTPBearer()

class UserRegister(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    department: Optional[str] = None
    year: Optional[int] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    user_id: str
    password: str

class UserProfile(BaseModel):
    user_id: str
    email: str
    full_name: str
    department: Optional[str]
    year: Optional[int]
    phone: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    conversation_count: int

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserProfile

# In-memory user store for demo (replace with actual database)
DEMO_USERS = {
    "student123": {
        "user_id": "student123",
        "email": "student@college.edu",
        "full_name": "John Doe",
        "department": "Computer Science",
        "year": 3,
        "phone": "+91-9876543210",
        "password_hash": "demo_hash",
        "created_at": datetime.now(),
        "last_login": None
    },
    "faculty456": {
        "user_id": "faculty456", 
        "email": "faculty@college.edu",
        "full_name": "Dr. Jane Smith",
        "department": "Computer Science",
        "year": None,
        "phone": "+91-9876543211",
        "password_hash": "demo_hash",
        "created_at": datetime.now(),
        "last_login": None
    }
}

# In-memory session store for demo
ACTIVE_SESSIONS = {}

def create_access_token(user_id: str) -> str:
    """Create a simple access token for demo purposes"""
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {
        "user_id": user_id,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    return token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify access token and return user_id"""
    token = credentials.credentials
    
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    session = ACTIVE_SESSIONS[token]
    if datetime.now() > session["expires_at"]:
        del ACTIVE_SESSIONS[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    
    return session["user_id"]

@router.post("/auth/register", response_model=AuthResponse)
async def register_user(user_data: UserRegister):
    """Register a new user (demo implementation)"""
    if user_data.user_id in DEMO_USERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID already exists"
        )
    
    # Add user to demo store
    DEMO_USERS[user_data.user_id] = {
        "user_id": user_data.user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "department": user_data.department,
        "year": user_data.year,
        "phone": user_data.phone,
        "password_hash": "demo_hash",  # In production, hash the actual password
        "created_at": datetime.now(),
        "last_login": None
    }
    
    # Create access token
    access_token = create_access_token(user_data.user_id)
    
    user_profile = UserProfile(
        user_id=user_data.user_id,
        email=user_data.email,
        full_name=user_data.full_name,
        department=user_data.department,
        year=user_data.year,
        phone=user_data.phone,
        created_at=datetime.now(),
        last_login=None,
        conversation_count=0
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400,  # 24 hours
        user=user_profile
    )

@router.post("/auth/login", response_model=AuthResponse)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    if login_data.user_id not in DEMO_USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID or password"
        )
    
    user = DEMO_USERS[login_data.user_id]
    
    # In production, verify password hash
    if login_data.password != "demo123":  # Demo password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID or password"
        )
    
    # Update last login
    user["last_login"] = datetime.now()
    
    # Count user's conversations
    from ..models.models import Thread
    conversation_count = db.query(Thread).filter(Thread.user_id == login_data.user_id).count()
    
    # Create access token
    access_token = create_access_token(login_data.user_id)
    
    user_profile = UserProfile(
        user_id=user["user_id"],
        email=user["email"],
        full_name=user["full_name"],
        department=user["department"],
        year=user["year"],
        phone=user["phone"],
        created_at=user["created_at"],
        last_login=user["last_login"],
        conversation_count=conversation_count
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400,
        user=user_profile
    )

@router.get("/auth/profile", response_model=UserProfile)
async def get_user_profile(current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user's profile"""
    if current_user not in DEMO_USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = DEMO_USERS[current_user]
    
    # Count user's conversations
    from ..models.models import Thread
    conversation_count = db.query(Thread).filter(Thread.user_id == current_user).count()
    
    return UserProfile(
        user_id=user["user_id"],
        email=user["email"], 
        full_name=user["full_name"],
        department=user["department"],
        year=user["year"],
        phone=user["phone"],
        created_at=user["created_at"],
        last_login=user["last_login"],
        conversation_count=conversation_count
    )

@router.post("/auth/logout")
async def logout_user(current_user: str = Depends(verify_token)):
    """Logout user and invalidate token"""
    # Find and remove the token
    for token, session in list(ACTIVE_SESSIONS.items()):
        if session["user_id"] == current_user:
            del ACTIVE_SESSIONS[token]
            break
    
    return {"message": "Successfully logged out"}

@router.get("/auth/demo-users")
async def get_demo_users():
    """Get list of demo users for testing"""
    return {
        "demo_users": [
            {
                "user_id": "student123",
                "password": "demo123",
                "role": "student",
                "full_name": "John Doe"
            },
            {
                "user_id": "faculty456",
                "password": "demo123", 
                "role": "faculty",
                "full_name": "Dr. Jane Smith"
            }
        ],
        "note": "Use these credentials for testing the authentication system"
    }
