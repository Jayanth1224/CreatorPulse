"""
LinkedIn Integration Router
Handles LinkedIn OAuth and posting
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
from app.services.linkedin_service import LinkedInService
from app.database import get_db, SupabaseDB
import secrets

router = APIRouter()
linkedin_service = LinkedInService()


class LinkedInPostRequest(BaseModel):
    """Request model for posting to LinkedIn"""
    draft_id: str
    content: str
    visibility: str = "PUBLIC"  # PUBLIC, CONNECTIONS, LOGGED_IN


class LinkedInAuthResponse(BaseModel):
    """Response model for LinkedIn OAuth"""
    authorization_url: str
    state: str


@router.get("/auth/url", response_model=LinkedInAuthResponse)
async def get_linkedin_auth_url(redirect_uri: str = Query(...)):
    """
    Get LinkedIn OAuth authorization URL
    
    Args:
        redirect_uri: The callback URL for OAuth
    
    Returns:
        Authorization URL and state token
    """
    try:
        state = secrets.token_urlsafe(32)
        auth_url = linkedin_service.get_oauth_url(redirect_uri, state)
        
        return {
            "authorization_url": auth_url,
            "state": state
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[ERROR] Failed to generate auth URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate auth URL: {str(e)}")


@router.post("/auth/callback")
async def linkedin_oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
    redirect_uri: str = Query(...),
    user_id: str = "00000000-0000-0000-0000-000000000001"
):
    """
    Handle LinkedIn OAuth callback
    
    Args:
        code: Authorization code from LinkedIn
        state: State token for CSRF protection
        redirect_uri: The callback URL
        user_id: The user ID to store credentials for
    
    Returns:
        Success status and access token info
    """
    try:
        # Exchange code for access token
        token_data = await linkedin_service.exchange_code_for_token(code, redirect_uri)
        
        if not token_data:
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        
        # Store access token in user settings (encrypted in production)
        # For MVP, we'll store it in user table
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # TODO: Encrypt the access token before storing
        # For now, store it as-is (NOT RECOMMENDED FOR PRODUCTION)
        db.table("users").update({
            "linkedin_access_token": token_data.get("access_token"),
            "linkedin_token_expires": token_data.get("expires_in")
        }).eq("id", user_id).execute()
        
        return {
            "success": True,
            "message": "LinkedIn account connected successfully",
            "expires_in": token_data.get("expires_in")
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] OAuth callback failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")


@router.post("/post")
async def post_to_linkedin(
    request: LinkedInPostRequest,
    user_id: str = "00000000-0000-0000-0000-000000000001"
):
    """
    Post content to LinkedIn (text-only for MVP)
    
    Args:
        request: Post request with draft_id, content, and visibility
        user_id: The user making the post
    
    Returns:
        Success status and LinkedIn post ID
    """
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Get user's LinkedIn access token
        user_response = db.table("users").select("linkedin_access_token").eq("id", user_id).execute()
        
        if not user_response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        access_token = user_response.data[0].get("linkedin_access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="LinkedIn account not connected. Please authorize first."
            )
        
        # Post to LinkedIn
        result = await linkedin_service.post_to_linkedin(
            access_token=access_token,
            text_content=request.content,
            visibility=request.visibility
        )
        
        if result.get("success"):
            # Update draft status to mark as posted to LinkedIn
            db.table("drafts").update({
                "status": "posted_linkedin",
                "linkedin_post_id": result.get("post_id")
            }).eq("id", request.draft_id).eq("user_id", user_id).execute()
            
            return {
                "success": True,
                "message": "Posted to LinkedIn successfully",
                "post_id": result.get("post_id"),
                "draft_id": request.draft_id
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to post to LinkedIn")
            )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to post to LinkedIn: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to post to LinkedIn: {str(e)}")


@router.delete("/disconnect")
async def disconnect_linkedin(user_id: str = "00000000-0000-0000-0000-000000000001"):
    """
    Disconnect LinkedIn account
    
    Args:
        user_id: The user disconnecting their account
    
    Returns:
        Success status
    """
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        db.table("users").update({
            "linkedin_access_token": None,
            "linkedin_token_expires": None
        }).eq("id", user_id).execute()
        
        return {
            "success": True,
            "message": "LinkedIn account disconnected"
        }
    
    except Exception as e:
        print(f"[ERROR] Failed to disconnect LinkedIn: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to disconnect: {str(e)}")


@router.get("/status")
async def get_linkedin_status(user_id: str = "00000000-0000-0000-0000-000000000001"):
    """
    Check if user has LinkedIn connected
    
    Args:
        user_id: The user to check
    
    Returns:
        Connection status
    """
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        user_response = db.table("users").select("linkedin_access_token").eq("id", user_id).execute()
        
        if not user_response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        is_connected = bool(user_response.data[0].get("linkedin_access_token"))
        
        return {
            "connected": is_connected,
            "message": "LinkedIn connected" if is_connected else "LinkedIn not connected"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to check LinkedIn status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check status: {str(e)}")

