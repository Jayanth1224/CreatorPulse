from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.utils.auth import get_current_user
from app.services.auto_newsletter_service import AutoNewsletterService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advanced-auto-newsletter", tags=["Advanced Auto Newsletter"])

# Pydantic models for advanced features

class CustomScheduleConfig(BaseModel):
    schedule_type: str = Field(..., description="Type of schedule: interval, business_hours, content_based, trend_based, custom_cron")
    schedule_config: Dict[str, Any] = Field(..., description="Configuration for the schedule")
    timezone: str = Field(default="America/Los_Angeles", description="Timezone for the schedule")

class TrendDetectionConfig(BaseModel):
    enabled: bool = Field(default=False, description="Enable trend detection")
    keywords: List[str] = Field(default=[], description="Keywords to track for trends")
    sources: List[str] = Field(default=[], description="Additional sources for trend data")

class SpikeDetectionConfig(BaseModel):
    enabled: bool = Field(default=False, description="Enable spike detection")
    threshold: float = Field(default=2.0, description="Spike detection threshold")
    timeframe_hours: int = Field(default=24, description="Timeframe for spike detection")

class AdvancedAutoNewsletterCreate(BaseModel):
    user_id: str
    bundle_id: str
    schedule_time: str = "08:00:00"
    schedule_frequency: str = "daily"
    schedule_day: Optional[int] = None
    email_recipients: List[str] = []
    timezone: str = "America/Los_Angeles"
    trend_detection: TrendDetectionConfig = TrendDetectionConfig()
    spike_detection: SpikeDetectionConfig = SpikeDetectionConfig()

class AdvancedAutoNewsletterUpdate(BaseModel):
    schedule_time: Optional[str] = None
    schedule_frequency: Optional[str] = None
    schedule_day: Optional[int] = None
    email_recipients: Optional[List[str]] = None
    timezone: Optional[str] = None
    trend_detection: Optional[TrendDetectionConfig] = None
    spike_detection: Optional[SpikeDetectionConfig] = None
    is_active: Optional[bool] = None

# API Endpoints

@router.post("/create")
async def create_advanced_auto_newsletter(
    newsletter_data: AdvancedAutoNewsletterCreate,
    current_user = Depends(get_current_user)
):
    """Create an advanced auto-newsletter with trend detection, spike detection, and custom scheduling"""
    try:
        service = AutoNewsletterService()
        
        # Create the auto-newsletter with advanced features
        newsletter = await service.create_auto_newsletter(
            user_id=newsletter_data.user_id,
            bundle_id=newsletter_data.bundle_id,
            schedule_time=newsletter_data.schedule_time,
            schedule_frequency=newsletter_data.schedule_frequency,
            schedule_day=newsletter_data.schedule_day,
            email_recipients=newsletter_data.email_recipients,
            timezone=newsletter_data.timezone,
            trend_detection_enabled=newsletter_data.trend_detection.enabled,
            trend_keywords=newsletter_data.trend_detection.keywords,
            spike_detection_enabled=newsletter_data.spike_detection.enabled,
            spike_threshold=newsletter_data.spike_detection.threshold,
            spike_timeframe_hours=newsletter_data.spike_detection.timeframe_hours
        )
        
        return {
            "success": True,
            "message": "Advanced auto-newsletter created successfully",
            "newsletter": newsletter
        }
        
    except Exception as e:
        logger.error(f"Error creating advanced auto-newsletter: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{auto_newsletter_id}/custom-schedule")
async def create_custom_schedule(
    auto_newsletter_id: str,
    schedule_config: CustomScheduleConfig,
    current_user = Depends(get_current_user)
):
    """Create a custom schedule for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        result = await service.create_custom_schedule(
            auto_newsletter_id=auto_newsletter_id,
            schedule_type=schedule_config.schedule_type,
            schedule_config=schedule_config.schedule_config,
            timezone=schedule_config.timezone
        )
        
        return {
            "success": True,
            "message": "Custom schedule created successfully",
            "schedule": result
        }
        
    except Exception as e:
        logger.error(f"Error creating custom schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/trends")
async def get_trends(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Get trending topics for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        trends = await service.detect_trends_for_newsletter(auto_newsletter_id)
        
        return {
            "success": True,
            "trends": trends
        }
        
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/spikes")
async def get_spikes(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Get content spikes for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        spikes = await service.detect_spikes_for_newsletter(auto_newsletter_id)
        
        return {
            "success": True,
            "spikes": spikes
        }
        
    except Exception as e:
        logger.error(f"Error getting spikes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{auto_newsletter_id}/generate-advanced")
async def generate_advanced_newsletter(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Generate newsletter with advanced features (trends, spikes, analytics)"""
    try:
        service = AutoNewsletterService()
        
        draft = await service.generate_advanced_newsletter(auto_newsletter_id)
        
        if not draft:
            raise HTTPException(status_code=404, detail="Auto-newsletter not found or inactive")
        
        return {
            "success": True,
            "message": "Advanced newsletter generated successfully",
            "draft": draft
        }
        
    except Exception as e:
        logger.error(f"Error generating advanced newsletter: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/analytics")
async def get_newsletter_analytics(
    auto_newsletter_id: str,
    days: int = 30,
    current_user = Depends(get_current_user)
):
    """Get comprehensive analytics for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        analytics = await service.get_newsletter_analytics(auto_newsletter_id, days)
        
        return {
            "success": True,
            "analytics": analytics
        }
        
    except Exception as e:
        logger.error(f"Error getting newsletter analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/trend-analytics")
async def get_trend_analytics(
    auto_newsletter_id: str,
    days: int = 30,
    current_user = Depends(get_current_user)
):
    """Get trend analytics for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        analytics = await service.get_trend_analytics(auto_newsletter_id, days)
        
        return {
            "success": True,
            "trend_analytics": analytics
        }
        
    except Exception as e:
        logger.error(f"Error getting trend analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/spike-analytics")
async def get_spike_analytics(
    auto_newsletter_id: str,
    days: int = 30,
    current_user = Depends(get_current_user)
):
    """Get spike analytics for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        analytics = await service.get_spike_analytics(auto_newsletter_id, days)
        
        return {
            "success": True,
            "spike_analytics": analytics
        }
        
    except Exception as e:
        logger.error(f"Error getting spike analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/schedule-analytics")
async def get_schedule_analytics(
    auto_newsletter_id: str,
    days: int = 30,
    current_user = Depends(get_current_user)
):
    """Get scheduling analytics for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        analytics = await service.get_schedule_analytics(auto_newsletter_id, days)
        
        return {
            "success": True,
            "schedule_analytics": analytics
        }
        
    except Exception as e:
        logger.error(f"Error getting schedule analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{auto_newsletter_id}/insights")
async def get_newsletter_insights(
    auto_newsletter_id: str,
    current_user = Depends(get_current_user)
):
    """Get actionable insights for an auto-newsletter"""
    try:
        service = AutoNewsletterService()
        
        insights = await service.get_newsletter_insights(auto_newsletter_id)
        
        return {
            "success": True,
            "insights": insights
        }
        
    except Exception as e:
        logger.error(f"Error getting newsletter insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-advanced")
async def process_advanced_scheduled_newsletters(
    current_user = Depends(get_current_user)
):
    """Process all auto-newsletters with advanced scheduling (admin endpoint)"""
    try:
        service = AutoNewsletterService()
        
        await service.process_advanced_scheduled_newsletters()
        
        return {
            "success": True,
            "message": "Advanced scheduled newsletters processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing advanced scheduled newsletters: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending-keywords")
async def get_trending_keywords(
    limit: int = 10,
    current_user = Depends(get_current_user)
):
    """Get currently trending keywords across all newsletters"""
    try:
        service = AutoNewsletterService()
        
        # This would need to be implemented in the trend detection service
        # For now, return a placeholder
        trending_keywords = [
            {"keyword": "AI", "trend_score": 8.5, "source": "google_trends"},
            {"keyword": "Machine Learning", "trend_score": 7.2, "source": "google_trends"},
            {"keyword": "Blockchain", "trend_score": 6.8, "source": "google_trends"},
        ]
        
        return {
            "success": True,
            "trending_keywords": trending_keywords[:limit]
        }
        
    except Exception as e:
        logger.error(f"Error getting trending keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
