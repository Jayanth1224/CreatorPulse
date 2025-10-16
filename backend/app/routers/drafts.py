from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.draft import (
    DraftResponse,
    GenerateDraftRequest,
    DraftUpdate,
    SendDraftRequest
)
from app.services.draft_generator import DraftGeneratorService
from app.database import get_db
import uuid

router = APIRouter()
draft_service = DraftGeneratorService()


@router.post("/generate", response_model=DraftResponse)
async def generate_draft(request: GenerateDraftRequest, user_id: str = "user-1"):
    """Generate a new newsletter draft from bundle"""
    try:
        print(f"[DRAFT] Starting generation for bundle {request.bundle_id}")
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
async def get_drafts(user_id: str = "user-1", status: str = None):
    """Get all drafts for a user"""
    # For MVP, return mock data
    # TODO: Fetch from Supabase
    mock_drafts = [
        {
            "id": "draft-1",
            "user_id": user_id,
            "bundle_id": "preset-1",
            "bundle_name": "AI & ML Trends",
            "topic": "AI content automation",
            "tone": "professional",
            "generated_html": "<p>Mock draft content</p>",
            "edited_html": None,
            "status": "draft",
            "readiness_score": 85,
            "sources": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "sent_at": None,
            "scheduled_for": None
        }
    ]
    return mock_drafts


@router.get("/{draft_id}", response_model=DraftResponse)
async def get_draft(draft_id: str, user_id: str = "user-1"):
    """Get a specific draft"""
    # For MVP, return mock data
    # TODO: Fetch from Supabase
    return {
        "id": draft_id,
        "user_id": user_id,
        "bundle_id": "preset-1",
        "bundle_name": "AI & ML Trends",
        "topic": "AI content automation",
        "tone": "professional",
        "generated_html": "<h2>Mock Draft</h2><p>This is a generated draft.</p>",
        "edited_html": None,
        "status": "draft",
        "readiness_score": 85,
        "sources": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "sent_at": None,
        "scheduled_for": None
    }


@router.patch("/{draft_id}", response_model=DraftResponse)
async def update_draft(draft_id: str, update: DraftUpdate, user_id: str = "user-1"):
    """Update a draft (autosave)"""
    # For MVP, return mock updated draft
    # TODO: Update in Supabase
    return {
        "id": draft_id,
        "user_id": user_id,
        "bundle_id": "preset-1",
        "bundle_name": "AI & ML Trends",
        "topic": "AI content automation",
        "tone": "professional",
        "generated_html": "<h2>Mock Draft</h2>",
        "edited_html": update.edited_html,
        "status": update.status or "draft",
        "readiness_score": 85,
        "sources": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "sent_at": None,
        "scheduled_for": update.scheduled_for
    }


@router.post("/{draft_id}/send")
async def send_draft(draft_id: str, request: SendDraftRequest, user_id: str = "user-1"):
    """Send a draft via email"""
    # For MVP, simulate sending
    # TODO: Implement ESP integration
    return {
        "success": True,
        "message": "Draft sent successfully",
        "draft_id": draft_id,
        "sent_to": request.recipients,
        "sent_at": datetime.now()
    }


@router.post("/{draft_id}/regenerate")
async def regenerate_section(draft_id: str, section: str = "intro", user_id: str = "user-1"):
    """Regenerate a specific section of the draft"""
    # For MVP, return mock regenerated content
    # TODO: Implement OpenAI regeneration
    return {
        "success": True,
        "section": section,
        "content": f"<h3>Regenerated {section}</h3><p>New content here...</p>"
    }


@router.post("/{draft_id}/reactions")
async def save_reaction(draft_id: str, section_id: str = None, reaction: str = "thumbs_up"):
    """Save user feedback reaction"""
    # For MVP, just acknowledge
    # TODO: Store in Supabase for learning
    return {
        "success": True,
        "message": "Feedback saved"
    }

