"""
Authentication utilities
JWT token verification and user authentication
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Callable
from app.config import settings
from app.database import get_db
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()


def create_access_token(user_id: str, email: str) -> str:
    """
    Create a JWT access token
    
    Args:
        user_id: User's ID
        email: User's email
    
    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    }
    
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
    
    Returns:
        User data dict
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    # Fetch user from database
    from app.database import SupabaseDB
    db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
    response = db.table("users").select("*").eq("id", user_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return response.data[0]


def get_optional_bearer():
    """Create optional HTTPBearer dependency"""
    return HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(get_optional_bearer)
) -> Optional[dict]:
    """
    Get current user if authenticated, otherwise return None
    Useful for optional authentication endpoints
    
    Args:
        credentials: HTTP Authorization credentials (optional)
    
    Returns:
        User data dict or None
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


def verify_supabase_jwt(token: str) -> Optional[dict]:
    """
    Verify Supabase JWT token
    
    Args:
        token: Supabase JWT token
    
    Returns:
        Decoded token payload or None
    """
    try:
        # Supabase JWTs use the service key as secret
        payload = jwt.decode(
            token,
            settings.supabase_service_key,
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload
    except Exception as e:
        print(f"[AUTH ERROR] Failed to verify Supabase JWT: {str(e)}")
        return None

