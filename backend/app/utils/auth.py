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
    Get current authenticated user from Supabase JWT token
    
    Args:
        credentials: HTTP Authorization credentials
    
    Returns:
        User data dict with at least 'id' and 'email' fields
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Verify Supabase JWT
    payload = verify_supabase_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Supabase JWT has 'sub' field which is the user ID
    user_id = payload.get("sub")
    email = payload.get("email")
    
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )
    
    # Ensure user exists in our users table (auto-create if needed)
    from app.database import SupabaseDB
    db = SupabaseDB.get_service_client()
    
    # Check if user exists
    existing_user = db.table("users").select("*").eq("id", user_id).execute()
    
    if not existing_user.data:
        # Auto-create user in our users table
        print(f"[AUTH] Auto-creating user {user_id} ({email}) in users table")
        try:
            db.table("users").insert({
                "id": user_id,
                "email": email,
                "name": email.split("@")[0],  # Use email prefix as default name
                "timezone": "UTC"
            }).execute()
        except Exception as e:
            print(f"[AUTH ERROR] Failed to create user: {str(e)}")
            # Continue anyway - the user exists in auth.users
    
    # Return user data from JWT
    return {
        "id": user_id,
        "email": email,
        **payload  # Include all JWT claims
    }


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
        # Supabase JWTs are signed with the project's JWT secret
        # Use settings.secret_key (mapped to Supabase JWT Secret in .env)
        # Skip audience and other claim validations for maximum compatibility
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": False,
                "verify_iat": False,
                "verify_aud": False,  # Skip audience verification
            }
        )
        return payload
    except Exception as e:
        print(f"[AUTH ERROR] Failed to verify Supabase JWT: {str(e)}")
        return None

