from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import RedirectResponse
from app.models.analytics import AnalyticsSummary
from app.database import get_db, SupabaseDB
from app.utils.auth import get_current_user
from typing import Optional
import base64

router = APIRouter()

# 1x1 transparent GIF for tracking pixel
TRANSPARENT_GIF = base64.b64decode(
    "R0lGODlhAQABAPAAAAAAAAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
)


@router.get("/", response_model=AnalyticsSummary)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Get analytics summary for user"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Get total drafts
        drafts_response = db.table("drafts").select("id", count="exact").eq("user_id", user_id).execute()
        total_drafts = drafts_response.count or 0
        
        # Get total sent
        sent_response = db.table("drafts").select("id", count="exact").eq("user_id", user_id).eq("status", "sent").execute()
        total_sent = sent_response.count or 0
        
        # Get analytics data
        analytics_response = db.table("analytics").select("*").execute()
        analytics_data = analytics_response.data
        
        # Calculate metrics
        total_emails_sent = len(analytics_data)
        total_opened = len([a for a in analytics_data if a.get("opened_at")])
        total_clicked = len([a for a in analytics_data if a.get("clicked_at")])
        
        open_rate = (total_opened / total_emails_sent * 100) if total_emails_sent > 0 else 0
        click_through_rate = (total_clicked / total_emails_sent * 100) if total_emails_sent > 0 else 0
        draft_acceptance_rate = (total_sent / total_drafts * 100) if total_drafts > 0 else 0
        
        return {
            "open_rate": round(open_rate, 1),
            "click_through_rate": round(click_through_rate, 1),
            "avg_review_time": 15.0,  # TODO: Track review time
            "draft_acceptance_rate": round(draft_acceptance_rate, 1),
            "total_drafts": total_drafts,
            "total_sent": total_sent
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")


@router.get("/drafts/{draft_id}")
async def get_draft_analytics(draft_id: str):
    """Get analytics for a specific draft"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Get analytics for this draft
        response = db.table("analytics").select("*").eq("draft_id", draft_id).execute()
        analytics_data = response.data
        
        if not analytics_data:
            return {
                "draft_id": draft_id,
                "opens": 0,
                "clicks": 0,
                "open_rate": 0,
                "click_rate": 0,
                "sent_at": None
            }
        
        total_sent = len(analytics_data)
        total_opened = len([a for a in analytics_data if a.get("opened_at")])
        total_clicked = len([a for a in analytics_data if a.get("clicked_at")])
        
        return {
            "draft_id": draft_id,
            "opens": total_opened,
            "clicks": total_clicked,
            "open_rate": round((total_opened / total_sent * 100) if total_sent > 0 else 0, 1),
            "click_rate": round((total_clicked / total_sent * 100) if total_sent > 0 else 0, 1),
            "sent_at": analytics_data[0].get("sent_at")
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch draft analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch draft analytics: {str(e)}")


@router.post("/track/open/{draft_id}")
async def track_email_open(draft_id: str, recipient_email: Optional[str] = None):
    """Track email open event"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Find the analytics record
        query = db.table("analytics").select("*").eq("draft_id", draft_id)
        if recipient_email:
            query = query.eq("recipient_email", recipient_email)
        
        response = query.execute()
        
        if response.data:
            # Update with opened_at timestamp
            from datetime import datetime
            db.table("analytics").update({
                "opened_at": datetime.now().isoformat()
            }).eq("id", response.data[0]["id"]).execute()
        
        return {"success": True, "message": "Open tracked"}
    except Exception as e:
        print(f"[ERROR] Failed to track open: {str(e)}")
        return {"success": False, "error": str(e)}


@router.post("/track/click/{draft_id}")
async def track_link_click(draft_id: str, recipient_email: Optional[str] = None):
    """Track link click event"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Find the analytics record
        query = db.table("analytics").select("*").eq("draft_id", draft_id)
        if recipient_email:
            query = query.eq("recipient_email", recipient_email)
        
        response = query.execute()
        
        if response.data:
            # Update with clicked_at timestamp
            from datetime import datetime
            db.table("analytics").update({
                "clicked_at": datetime.now().isoformat()
            }).eq("id", response.data[0]["id"]).execute()
        
        return {"success": True, "message": "Click tracked"}
    except Exception as e:
        print(f"[ERROR] Failed to track click: {str(e)}")
        return {"success": False, "error": str(e)}


@router.get("/track/open/{draft_id}")
async def track_email_open_get(draft_id: str, token: Optional[str] = None):
    """Track email open event via GET (for tracking pixel)"""
    try:
        db = SupabaseDB.get_service_client()
        
        # Find the analytics record
        query = db.table("analytics").select("*").eq("draft_id", draft_id)
        if token:
            query = query.eq("token", token)
        
        response = query.execute()
        
        if response.data:
            # Update with opened_at timestamp
            from datetime import datetime
            db.table("analytics").update({
                "opened_at": datetime.now().isoformat()
            }).eq("id", response.data[0]["id"]).execute()
        
        # Return 1x1 transparent GIF
        return Response(content=TRANSPARENT_GIF, media_type="image/gif")
    except Exception as e:
        print(f"[ERROR] Failed to track open: {str(e)}")
        # Still return a pixel to avoid broken images
        return Response(content=TRANSPARENT_GIF, media_type="image/gif")


@router.get("/track/click/{draft_id}")
async def track_link_click_get(draft_id: str, url: str, token: Optional[str] = None):
    """Track link click event via GET (for wrapped links)"""
    try:
        db = SupabaseDB.get_service_client()
        
        # Find the analytics record
        query = db.table("analytics").select("*").eq("draft_id", draft_id)
        if token:
            query = query.eq("token", token)
        
        response = query.execute()
        
        if response.data:
            # Update with clicked_at timestamp
            from datetime import datetime
            db.table("analytics").update({
                "clicked_at": datetime.now().isoformat(),
                "last_clicked_url": url
            }).eq("id", response.data[0]["id"]).execute()
    except Exception as e:
        print(f"[ERROR] Failed to track click: {str(e)}")
    finally:
        # Always redirect to the original URL
        return RedirectResponse(url=url, status_code=302)

