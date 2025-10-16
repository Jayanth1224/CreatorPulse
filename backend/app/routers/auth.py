from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.models.user import UserCreate, UserResponse
from app.database import get_db, SupabaseDB
from app.utils.auth import create_access_token, get_current_user
from typing import Optional

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str
    user: UserResponse


@router.post("/signup", response_model=LoginResponse)
async def signup(user: UserCreate):
    """Register a new user"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Check if user already exists
        existing_user = db.table("users").select("*").eq("email", user.email).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user in Supabase Auth
        # Note: This uses Supabase's built-in auth
        # For production, you'd want to use supabase.auth.sign_up()
        
        # For MVP, create user directly in users table
        user_data = {
            "email": user.email,
            "name": user.name,
            "timezone": user.timezone or "America/Los_Angeles"
        }
        
        response = db.table("users").insert(user_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        new_user = response.data[0]
        
        # Create access token
        access_token = create_access_token(new_user["id"], new_user["email"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": new_user
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH ERROR] Signup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login user and return access token"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Find user by email
        user_response = db.table("users").select("*").eq("email", request.email).execute()
        
        if not user_response.data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = user_response.data[0]
        
        # For MVP, we're not validating passwords (Supabase Auth would handle this)
        # In production, use Supabase's supabase.auth.sign_in_with_password()
        
        # Create access token
        access_token = create_access_token(user["id"], user["email"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH ERROR] Login failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user


@router.post("/logout")
async def logout():
    """Logout user (client should delete token)"""
    return {
        "success": True,
        "message": "Logged out successfully"
    }


@router.put("/me")
async def update_profile(
    name: Optional[str] = None,
    timezone: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        update_data = {}
        if name:
            update_data["name"] = name
        if timezone:
            update_data["timezone"] = timezone
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        response = db.table("users").update(update_data).eq("id", current_user["id"]).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH ERROR] Profile update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(e)}")

