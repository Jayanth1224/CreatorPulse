from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from ..services.auto_newsletter_service import AutoNewsletterService
from ..utils.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auto-newsletters", tags=["auto-newsletters"])

# Pydantic models for request/response
class AutoNewsletterCreate(BaseModel):
    bundle_id: str
    schedule_time: str = "08:00:00"
    schedule_frequency: str = "daily"  # daily, weekly, monthly
    schedule_day: Optional[int] = None
    email_recipients: List[EmailStr] = []

class AutoNewsletterUpdate(BaseModel):
    is_active: Optional[bool] = None
    schedule_time: Optional[str] = None
    schedule_frequency: Optional[str] = None
    schedule_day: Optional[int] = None
    email_recipients: Optional[List[EmailStr]] = None

class AutoNewsletterResponse(BaseModel):
    id: str
    user_id: str
    bundle_id: str
    is_active: bool
    schedule_time: str
    schedule_frequency: str
    schedule_day: Optional[int]
    email_recipients: List[str]
    last_generated: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[AutoNewsletterResponse])
async def get_auto_newsletters(current_user = Depends(get_current_user)):
    """Get all auto-newsletters for the current user"""
    try:
        service = AutoNewsletterService()
        auto_newsletters = await service.get_user_auto_newsletters(current_user['id'])
        
        return [AutoNewsletterResponse(**auto_newsletter) for auto_newsletter in auto_newsletters]
    
    except Exception as e:
        logger.error(f"Failed to get auto-newsletters: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve auto-newsletters"
        )

@router.post("/", response_model=AutoNewsletterResponse)
async def create_auto_newsletter(
    auto_newsletter_data: AutoNewsletterCreate,
    current_user = Depends(get_current_user)
):
    """Create a new auto-newsletter configuration"""
    try:
        service = AutoNewsletterService()
        
        # Validate schedule_day based on frequency
        if auto_newsletter_data.schedule_frequency == "weekly":
            if not auto_newsletter_data.schedule_day or not (1 <= auto_newsletter_data.schedule_day <= 7):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="schedule_day must be between 1-7 for weekly frequency"
                )
        elif auto_newsletter_data.schedule_frequency == "monthly":
            if not auto_newsletter_data.schedule_day or not (1 <= auto_newsletter_data.schedule_day <= 31):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="schedule_day must be between 1-31 for monthly frequency"
                )
        
        auto_newsletter = await service.create_auto_newsletter(
            user_id=current_user['id'],
            bundle_id=auto_newsletter_data.bundle_id,
            schedule_time=auto_newsletter_data.schedule_time,
            schedule_frequency=auto_newsletter_data.schedule_frequency,
            schedule_day=auto_newsletter_data.schedule_day,
            email_recipients=[email for email in auto_newsletter_data.email_recipients]
        )
        
        return AutoNewsletterResponse(**auto_newsletter)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create auto-newsletter: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create auto-newsletter: {str(e)}"
        )

@router.get("/{auto_newsletter_id}", response_model=AutoNewsletterResponse)
async def get_auto_newsletter(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Get a specific auto-newsletter by ID"""
    try:
        service = AutoNewsletterService()
        auto_newsletters = await service.get_user_auto_newsletters(current_user['id'])
        
        # Find the specific auto-newsletter
        auto_newsletter = next(
            (an for an in auto_newsletters if str(an.get('id')) == auto_newsletter_id), 
            None
        )
        
        if not auto_newsletter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        return AutoNewsletterResponse(**auto_newsletter)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get auto-newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve auto-newsletter"
        )

@router.put("/{auto_newsletter_id}", response_model=AutoNewsletterResponse)
async def update_auto_newsletter(
    auto_newsletter_id: str,
    auto_newsletter_data: AutoNewsletterUpdate,
    current_user = Depends(get_current_user)
):
    """Update an auto-newsletter configuration"""
    try:
        service = AutoNewsletterService()
        
        # Check if auto-newsletter exists and belongs to user
        auto_newsletters = await service.get_user_auto_newsletters(current_user['id'])
        auto_newsletter = next(
            (an for an in auto_newsletters if str(an.get('id')) == auto_newsletter_id), 
            None
        )
        
        if not auto_newsletter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        # Prepare update data
        update_data = {}
        for field, value in auto_newsletter_data.dict(exclude_unset=True).items():
            if value is not None:
                update_data[field] = value
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        updated_auto_newsletter = await service.update_auto_newsletter(
            auto_newsletter_id, 
            **update_data
        )
        
        if not updated_auto_newsletter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        return AutoNewsletterResponse(**updated_auto_newsletter)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update auto-newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update auto-newsletter"
        )

@router.delete("/{auto_newsletter_id}")
async def delete_auto_newsletter(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Delete an auto-newsletter configuration"""
    try:
        service = AutoNewsletterService()
        
        # Check if auto-newsletter exists and belongs to user
        auto_newsletters = await service.get_user_auto_newsletters(current_user['id'])
        auto_newsletter = next(
            (an for an in auto_newsletters if str(an.get('id')) == auto_newsletter_id), 
            None
        )
        
        if not auto_newsletter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        success = await service.delete_auto_newsletter(auto_newsletter_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        return {"message": "Auto-newsletter deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete auto-newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete auto-newsletter"
        )

@router.post("/{auto_newsletter_id}/generate")
async def generate_newsletter_now(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Manually trigger newsletter generation for testing"""
    try:
        service = AutoNewsletterService()
        
        # Check if auto-newsletter exists and belongs to user
        auto_newsletters = await service.get_user_auto_newsletters(current_user['id'])
        auto_newsletter = next(
            (an for an in auto_newsletters if str(an.get('id')) == auto_newsletter_id), 
            None
        )
        
        if not auto_newsletter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Auto-newsletter not found"
            )
        
        draft = await service.generate_auto_newsletter(auto_newsletter_id)
        
        if not draft:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate newsletter"
            )
        
        return {
            "message": "Newsletter generated successfully",
            "draft_id": str(draft.get('id')),
            "draft_url": f"/create/{draft.get('id')}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate newsletter"
        )
