from fastapi import APIRouter
from app.models.analytics import AnalyticsSummary
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=AnalyticsSummary)
async def get_analytics(user_id: str = "user-1"):
    """Get analytics summary for user"""
    # For MVP, return mock analytics
    # TODO: Calculate from Supabase analytics table
    return {
        "open_rate": 42.5,
        "click_through_rate": 8.3,
        "avg_review_time": 18.5,
        "draft_acceptance_rate": 73.2,
        "total_drafts": 45,
        "total_sent": 33
    }


@router.get("/drafts/{draft_id}")
async def get_draft_analytics(draft_id: str):
    """Get analytics for a specific draft"""
    # For MVP, return mock draft analytics
    # TODO: Fetch from Supabase
    return {
        "draft_id": draft_id,
        "opens": 125,
        "clicks": 23,
        "open_rate": 41.2,
        "click_rate": 7.6,
        "sent_at": "2025-10-15T10:00:00Z"
    }

