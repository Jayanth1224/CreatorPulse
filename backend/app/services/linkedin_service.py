"""
LinkedIn API Integration Service
Handles posting content to LinkedIn
"""
import httpx
from typing import Dict, Optional
from app.config import settings


class LinkedInService:
    """Service for posting to LinkedIn"""
    
    def __init__(self):
        self.api_base_url = "https://api.linkedin.com/v2"
    
    async def post_to_linkedin(
        self,
        access_token: str,
        text_content: str,
        visibility: str = "PUBLIC"
    ) -> Dict:
        """
        Post text-only content to LinkedIn
        
        Args:
            access_token: User's LinkedIn OAuth access token
            text_content: The text content to post
            visibility: Post visibility (PUBLIC, CONNECTIONS, LOGGED_IN)
        
        Returns:
            Dict with post_id and success status
        """
        try:
            # First, get the user's profile URN
            profile_urn = await self._get_user_profile_urn(access_token)
            
            if not profile_urn:
                raise Exception("Failed to get user profile URN")
            
            # Prepare the post payload
            post_payload = {
                "author": profile_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text_content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            # Post to LinkedIn
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/ugcPosts",
                    json=post_payload,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code in [200, 201]:
                    post_data = response.json()
                    return {
                        "success": True,
                        "post_id": post_data.get("id"),
                        "message": "Posted to LinkedIn successfully"
                    }
                else:
                    error_detail = response.text
                    print(f"[LINKEDIN ERROR] {response.status_code}: {error_detail}")
                    return {
                        "success": False,
                        "error": f"LinkedIn API error: {response.status_code}",
                        "details": error_detail
                    }
        
        except Exception as e:
            print(f"[LINKEDIN ERROR] Failed to post: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_user_profile_urn(self, access_token: str) -> Optional[str]:
        """Get the authenticated user's LinkedIn profile URN"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/me",
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return f"urn:li:person:{user_data.get('id')}"
                else:
                    print(f"[LINKEDIN ERROR] Failed to get profile: {response.status_code}")
                    return None
        
        except Exception as e:
            print(f"[LINKEDIN ERROR] Failed to get profile URN: {str(e)}")
            return None
    
    def get_oauth_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate LinkedIn OAuth URL for user authorization
        
        Args:
            redirect_uri: The callback URL after authorization
            state: Random state for CSRF protection
        
        Returns:
            OAuth authorization URL
        """
        # You'll need to add LINKEDIN_CLIENT_ID to settings
        client_id = getattr(settings, 'linkedin_client_id', None)
        
        if not client_id:
            raise ValueError("LinkedIn client ID not configured")
        
        scope = "w_member_social"  # Permission to post on behalf of user
        
        return (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&scope={scope}"
        )
    
    async def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str
    ) -> Optional[Dict]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from OAuth callback
            redirect_uri: The same redirect URI used in authorization
        
        Returns:
            Dict with access_token and expires_in
        """
        try:
            client_id = getattr(settings, 'linkedin_client_id', None)
            client_secret = getattr(settings, 'linkedin_client_secret', None)
            
            if not client_id or not client_secret:
                raise ValueError("LinkedIn credentials not configured")
            
            payload = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://www.linkedin.com/oauth/v2/accessToken",
                    data=payload,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"[LINKEDIN ERROR] Token exchange failed: {response.status_code}")
                    return None
        
        except Exception as e:
            print(f"[LINKEDIN ERROR] Failed to exchange code: {str(e)}")
            return None

