from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse
from app.database import get_db

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    """Register a new user"""
    # For MVP, this is a placeholder
    # TODO: Implement Supabase Auth integration
    return {
        "id": "user-1",
        "email": user.email,
        "name": user.name,
        "timezone": user.timezone,
        "created_at": "2025-10-16T00:00:00Z"
    }


@router.post("/login")
async def login(email: str, password: str):
    """Login user and return access token"""
    # For MVP, this is a placeholder
    # TODO: Implement Supabase Auth integration
    return {
        "access_token": "mock-token",
        "token_type": "bearer",
        "user": {
            "id": "user-1",
            "email": email,
            "name": "Test User"
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current authenticated user"""
    # For MVP, this is a placeholder
    # TODO: Implement JWT token validation
    return {
        "id": "user-1",
        "email": "user@example.com",
        "name": "Test User",
        "timezone": "America/Los_Angeles",
        "created_at": "2025-10-16T00:00:00Z"
    }

