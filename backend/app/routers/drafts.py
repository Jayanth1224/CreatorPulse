from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from app.models.draft import (
    DraftResponse,
    GenerateDraftRequest,
    DraftUpdate,
    SendDraftRequest
)
from app.services.draft_generator import DraftGeneratorService
from app.database import get_db, SupabaseDB
from app.utils.auth import get_current_user
import uuid

router = APIRouter()
draft_service = DraftGeneratorService()


@router.post("/generate", response_model=DraftResponse)
async def generate_draft(request: GenerateDraftRequest, current_user: dict = Depends(get_current_user)):
    """Generate a new newsletter draft from bundle"""
    try:
        user_id = current_user["id"]
        print(f"[DRAFT] Starting generation for user {user_id}, bundle {request.bundle_id}")
        draft = await draft_service.generate_draft(
            user_id=user_id,
            bundle_id=request.bundle_id,
            topic=request.topic,
            tone=request.tone
        )
        print(f"[DRAFT] Successfully generated draft {draft['id']}")
        return draft
    except Exception as e:
        print(f"[DRAFT ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate draft: {str(e)}")


@router.get("/", response_model=List[DraftResponse])
async def get_drafts(current_user: dict = Depends(get_current_user), status: Optional[str] = None):
    """Get all drafts for a user"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        query = db.table("drafts").select("*").eq("user_id", user_id)
        
        if status:
            query = query.eq("status", status)
        
        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"[ERROR] Failed to fetch drafts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch drafts: {str(e)}")


@router.get("/{draft_id}", response_model=DraftResponse)
async def get_draft(draft_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific draft"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("drafts").select("*").eq("id", draft_id).eq("user_id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch draft: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch draft: {str(e)}")


@router.patch("/{draft_id}", response_model=DraftResponse)
async def update_draft(draft_id: str, update: DraftUpdate, current_user: dict = Depends(get_current_user)):
    """Update a draft (autosave)"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Build update data
        update_data = {}
        if update.edited_html is not None:
            update_data["edited_html"] = update.edited_html
        if update.status is not None:
            update_data["status"] = update.status
        if update.scheduled_for is not None:
            update_data["scheduled_for"] = update.scheduled_for.isoformat()
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        response = db.table("drafts").update(update_data).eq("id", draft_id).eq("user_id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to update draft: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update draft: {str(e)}")


@router.delete("/{draft_id}")
async def delete_draft(draft_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a draft"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("drafts").delete().eq("id", draft_id).eq("user_id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        return {"success": True, "message": "Draft deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete draft: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete draft: {str(e)}")


@router.post("/{draft_id}/send")
async def send_draft(draft_id: str, request: SendDraftRequest, current_user: dict = Depends(get_current_user)):
    """Send a draft via email"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        # Get draft
        draft_response = db.table("drafts").select("*").eq("id", draft_id).eq("user_id", user_id).execute()
        if not draft_response.data:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        draft = draft_response.data[0]
        
        # Send email using email service
        from app.services.email_service import EmailService
        email_service = EmailService()
        
        # Use edited_html if available, otherwise use generated_html
        html_content = draft.get("edited_html") or draft.get("generated_html")
        subject = draft.get("topic") or draft.get("bundle_name", "Newsletter")
        
        send_result = await email_service.send_newsletter(
            recipients=request.recipients,
            subject=subject,
            html_content=html_content,
            draft_id=draft_id
        )
        
        if send_result.get("success"):
            # Mark as sent
            sent_at = datetime.now().isoformat()
            db.table("drafts").update({
                "status": "sent",
                "sent_at": sent_at
            }).eq("id", draft_id).execute()
            
            # Create analytics entries for tracking
            for recipient in request.recipients:
                db.table("analytics").insert({
                    "draft_id": draft_id,
                    "sent_at": sent_at,
                    "recipient_email": recipient
                }).execute()
            
            return {
                "success": True,
                "message": "Draft sent successfully",
                "draft_id": draft_id,
                "sent_to": request.recipients,
                "sent_at": sent_at,
                "method": send_result.get("method", "unknown")
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send email: {send_result.get('error', 'Unknown error')}"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to send draft: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send draft: {str(e)}")


@router.post("/{draft_id}/regenerate")
async def regenerate_section(draft_id: str, section: str = "intro", current_user: dict = Depends(get_current_user)):
    """Regenerate a specific section of the draft"""
    # For MVP, return mock regenerated content
    # TODO: Implement OpenAI regeneration
    return {
        "success": True,
        "section": section,
        "content": f"<h3>Regenerated {section}</h3><p>New content here...</p>"
    }


@router.post("/{draft_id}/reactions")
async def save_reaction(draft_id: str, section_id: str = None, reaction: str = "thumbs_up", current_user: dict = Depends(get_current_user)):
    """Save user feedback reaction"""
    try:
        user_id = current_user["id"]
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        db.table("feedback").insert({
            "draft_id": draft_id,
            "section_id": section_id,
            "reaction": reaction,
            "user_id": user_id
        }).execute()
        
        return {
            "success": True,
            "message": "Feedback saved"
        }
    except Exception as e:
        print(f"[ERROR] Failed to save reaction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save reaction: {str(e)}")

