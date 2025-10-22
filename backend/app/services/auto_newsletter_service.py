import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.database import SupabaseDB
from .draft_generator import DraftGeneratorService
from .email_service import EmailService
from .trend_detection_service import TrendDetectionService
from .spike_detection_service import SpikeDetectionService
from .advanced_scheduling_service import AdvancedSchedulingService
from .auto_newsletter_analytics_service import AutoNewsletterAnalyticsService
import logging

logger = logging.getLogger(__name__)

class AutoNewsletterService:
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
        self.draft_generator = DraftGeneratorService()
        self.email_service = EmailService()
        self.trend_detection = TrendDetectionService()
        self.spike_detection = SpikeDetectionService()
        self.advanced_scheduling = AdvancedSchedulingService()
        self.analytics = AutoNewsletterAnalyticsService()
    
    async def create_auto_newsletter(
        self,
        user_id: str,
        bundle_id: str,
        schedule_time: str = "08:00:00",
        schedule_frequency: str = "daily",
        schedule_day: Optional[int] = None,
        email_recipients: Optional[List[str]] = None,
        timezone: str = "America/Los_Angeles",
        trend_detection_enabled: bool = False,
        trend_keywords: Optional[List[str]] = None,
        spike_detection_enabled: bool = False,
        spike_threshold: float = 2.0,
        spike_timeframe_hours: int = 24
    ) -> Dict[str, Any]:
        try:
            data = {
                "user_id": user_id,
                "bundle_id": bundle_id,
                "schedule_time": schedule_time,
                "schedule_frequency": schedule_frequency,
                "schedule_day": schedule_day,
                "email_recipients": email_recipients or [],
                "timezone": timezone,
                "trend_detection_enabled": trend_detection_enabled,
                "trend_keywords": trend_keywords or [],
                "spike_detection_enabled": spike_detection_enabled,
                "spike_threshold": spike_threshold,
                "spike_timeframe_hours": spike_timeframe_hours,
            }
            logger.info(f"Creating auto-newsletter with data: {data}")
            res = self.db.table("auto_newsletters").insert(data).execute()
            logger.info(f"Supabase insert response: {res}")
            if not res.data:
                raise Exception(f"No data returned from insert. Response: {res}")
            return res.data[0]
        except Exception as e:
            logger.error(f"Error in create_auto_newsletter: {str(e)}")
            logger.error(f"Data attempted: {data}")
            raise
    
    async def get_user_auto_newsletters(self, user_id: str) -> List[Dict[str, Any]]:
        res = self.db.table("auto_newsletters").select("*").eq("user_id", user_id).execute()
        return res.data or []
    
    async def get_active_auto_newsletters(self) -> List[Dict[str, Any]]:
        res = self.db.table("auto_newsletters").select("*").eq("is_active", True).execute()
        return res.data or []
    
    async def update_auto_newsletter(self, auto_newsletter_id: str, **updates) -> Optional[Dict[str, Any]]:
        res = self.db.table("auto_newsletters").update(updates).eq("id", auto_newsletter_id).execute()
        if not res.data:
            return None
        return res.data[0]
    
    async def delete_auto_newsletter(self, auto_newsletter_id: str) -> bool:
        res = self.db.table("auto_newsletters").delete().eq("id", auto_newsletter_id).execute()
        return bool(res.data)
    
    async def generate_auto_newsletter(self, auto_newsletter_id: str) -> Optional[Dict[str, Any]]:
        res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
        auto_newsletter = res.data
        if not auto_newsletter or not auto_newsletter.get("is_active"):
            return None
        draft = await self.draft_generator.generate_draft(
            user_id=auto_newsletter["user_id"],
            bundle_id=auto_newsletter["bundle_id"],
            topic=f"Auto-generated newsletter - {datetime.now().strftime('%Y-%m-%d')}",
            tone="professional"
        )
        # Update last_generated
        self.db.table("auto_newsletters").update({"last_generated": datetime.now().isoformat()}).eq("id", auto_newsletter_id).execute()
        await self._send_notification_email(auto_newsletter, draft)
        return draft
    
    async def _send_notification_email(self, auto_newsletter: Dict[str, Any], draft: Dict[str, Any]):
        """Send notification email to auto-newsletter recipients"""
        
        if not auto_newsletter.get("email_recipients"):
            logger.warning(f"No email recipients for auto-newsletter {auto_newsletter.get('id')}")
            return
        
        # Create email content
        subject = f"📰 Your Auto-Newsletter is Ready - {draft.get('topic', 'Newsletter')}"
        
        # Get bundle name for email
        # Resolve bundle name from preset bundles
        from app.routers.bundles import PRESET_BUNDLES
        bundle = next((b for b in PRESET_BUNDLES if b["id"] == auto_newsletter["bundle_id"]), None)
        bundle_name = bundle["label"] if bundle else "Newsletter"
        
        html_content = f"""
        <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
            <h2>📰 Your Auto-Newsletter is Ready!</h2>
            
            <p>Hi there,</p>
            
            <p>Your auto-newsletter for <strong>{bundle_name}</strong> has been generated and is ready for review.</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>Newsletter Details:</h3>
                <ul>
                    <li><strong>Topic:</strong> {draft.get('topic', 'Newsletter')}</li>
                    <li><strong>Bundle:</strong> {bundle_name}</li>
                    <li><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{self._get_draft_url(draft.get('id'))}" 
                   style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Review & Edit Newsletter
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">
                Click the button above to review and edit your newsletter before sending it to your audience.
            </p>
        </div>
        """
        
        # Send email to all recipients
        for email in auto_newsletter["email_recipients"]:
            try:
                await self.email_service.send_test_email(
                    recipient=email,
                    subject=subject,
                    html_content=html_content
                )
                logger.info(f"Sent auto-newsletter notification to {email}")
            except Exception as e:
                logger.error(f"Failed to send notification to {email}: {str(e)}")
    
    def _get_draft_url(self, draft_id: str) -> str:
        """Generate the URL for editing a draft"""
        base_url = "http://localhost:3000"  # This should come from environment
        return f"{base_url}/create/{draft_id}"
    
    async def process_scheduled_newsletters(self):
        """Process all auto-newsletters that are due for generation"""
        
        active_newsletters = await self.get_active_auto_newsletters()
        current_time = datetime.now()
        
        for newsletter in active_newsletters:
            if self._should_generate_newsletter(newsletter, current_time):
                logger.info(f"Processing auto-newsletter {newsletter['id']}")
                await self.generate_auto_newsletter(str(newsletter["id"]))
    
    def _should_generate_newsletter(self, newsletter: Dict[str, Any], current_time: datetime) -> bool:
        """Check if a newsletter should be generated based on schedule"""
        
        # Parse schedule time
        schedule_hour, schedule_minute = map(int, str(newsletter.get("schedule_time", "08:00")).split(':')[:2])
        
        # Check if it's the right time
        if current_time.hour != schedule_hour or current_time.minute != schedule_minute:
            return False
        
        # Check frequency
        if newsletter.get("schedule_frequency") == "daily":
            return True
        elif newsletter.get("schedule_frequency") == "weekly":
            # Check if it's the right day of week (1=Monday, 7=Sunday)
            return current_time.weekday() + 1 == newsletter.get("schedule_day")
        elif newsletter.get("schedule_frequency") == "monthly":
            # Check if it's the right day of month
            return current_time.day == newsletter.get("schedule_day")
        
        return False
    
    # Advanced Features Methods
    
    async def create_custom_schedule(
        self,
        auto_newsletter_id: str,
        schedule_type: str,
        schedule_config: Dict[str, Any],
        timezone: str = "America/Los_Angeles"
    ) -> Dict[str, Any]:
        """Create a custom schedule for an auto-newsletter"""
        return await self.advanced_scheduling.create_custom_schedule(
            auto_newsletter_id, schedule_type, schedule_config, timezone
        )
    
    async def detect_trends_for_newsletter(self, auto_newsletter_id: str) -> List[Dict[str, Any]]:
        """Detect trends for a specific auto-newsletter"""
        try:
            # Get auto-newsletter configuration
            res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
            if not res.data:
                return []
            
            newsletter = res.data
            if not newsletter.get("trend_detection_enabled"):
                return []
            
            keywords = newsletter.get("trend_keywords", [])
            if not keywords:
                return []
            
            # Detect trends
            trends = await self.trend_detection.detect_trends_for_keywords(keywords)
            return trends
            
        except Exception as e:
            logger.error(f"Error detecting trends for newsletter {auto_newsletter_id}: {str(e)}")
            return []
    
    async def detect_spikes_for_newsletter(self, auto_newsletter_id: str) -> List[Dict[str, Any]]:
        """Detect content spikes for a specific auto-newsletter"""
        try:
            # Get auto-newsletter configuration
            res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
            if not res.data:
                return []
            
            newsletter = res.data
            if not newsletter.get("spike_detection_enabled"):
                return []
            
            threshold = newsletter.get("spike_threshold", 2.0)
            timeframe_hours = newsletter.get("spike_timeframe_hours", 24)
            
            # Detect spikes
            spikes = await self.spike_detection.detect_content_spikes(
                auto_newsletter_id, threshold, timeframe_hours
            )
            return spikes
            
        except Exception as e:
            logger.error(f"Error detecting spikes for newsletter {auto_newsletter_id}: {str(e)}")
            return []
    
    async def generate_advanced_newsletter(self, auto_newsletter_id: str) -> Optional[Dict[str, Any]]:
        """Generate newsletter with advanced features (trends, spikes, analytics)"""
        try:
            # Get auto-newsletter configuration
            res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
            auto_newsletter = res.data
            if not auto_newsletter or not auto_newsletter.get("is_active"):
                return None
            
            # Initialize analytics tracking
            content_quality_score = None
            trend_relevance_score = None
            spike_impact_score = None
            total_sources_used = 0
            unique_trends_detected = 0
            spike_events_processed = 0
            
            # Detect trends if enabled
            if auto_newsletter.get("trend_detection_enabled"):
                trends = await self.detect_trends_for_newsletter(auto_newsletter_id)
                unique_trends_detected = len(set(trend["keyword"] for trend in trends))
                if trends:
                    # Calculate trend relevance score
                    trend_relevance_score = await self.trend_detection.analyze_trend_relevance(
                        "", [trend["keyword"] for trend in trends]
                    )
            
            # Detect spikes if enabled
            if auto_newsletter.get("spike_detection_enabled"):
                spikes = await self.detect_spikes_for_newsletter(auto_newsletter_id)
                spike_events_processed = len(spikes)
                if spikes:
                    # Calculate spike impact score
                    spike_impact_score = sum(spike["spike_score"] for spike in spikes) / len(spikes)
            
            # Generate the newsletter draft
            draft = await self.draft_generator.generate_draft(
                user_id=auto_newsletter["user_id"],
                bundle_id=auto_newsletter["bundle_id"],
                topic=f"Auto-generated newsletter - {datetime.now().strftime('%Y-%m-%d')}",
                tone="professional"
            )
            
            # Calculate content quality score (placeholder)
            content_quality_score = 0.8  # This would be calculated based on content analysis
            
            # Track analytics
            await self.analytics.track_newsletter_generation(
                auto_newsletter_id=auto_newsletter_id,
                draft_id=draft.get("id"),
                content_quality_score=content_quality_score,
                trend_relevance_score=trend_relevance_score,
                spike_impact_score=spike_impact_score,
                total_sources_used=total_sources_used,
                unique_trends_detected=unique_trends_detected,
                spike_events_processed=spike_events_processed
            )
            
            # Update last_generated
            self.db.table("auto_newsletters").update({
                "last_generated": datetime.now().isoformat()
            }).eq("id", auto_newsletter_id).execute()
            
            # Send notification email
            await self._send_notification_email(auto_newsletter, draft)
            
            return draft
            
        except Exception as e:
            logger.error(f"Error generating advanced newsletter: {str(e)}")
            return None
    
    async def get_newsletter_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive analytics for an auto-newsletter"""
        return await self.analytics.get_comprehensive_analytics(auto_newsletter_id, days)
    
    async def get_trend_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get trend analytics for an auto-newsletter"""
        return await self.analytics.get_trend_analytics(auto_newsletter_id, days)
    
    async def get_spike_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get spike analytics for an auto-newsletter"""
        return await self.analytics.get_spike_analytics(auto_newsletter_id, days)
    
    async def get_schedule_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get scheduling analytics for an auto-newsletter"""
        return await self.advanced_scheduling.get_schedule_analytics(auto_newsletter_id, days)
    
    async def process_advanced_scheduled_newsletters(self):
        """Process all auto-newsletters with advanced scheduling"""
        try:
            # Get newsletters due for generation
            due_newsletters = await self.advanced_scheduling.get_scheduled_newsletters()
            
            for newsletter in due_newsletters:
                logger.info(f"Processing advanced auto-newsletter {newsletter['id']}")
                
                # Check if it's a content-based or trend-based trigger
                custom_schedule = newsletter.get("custom_schedule")
                if custom_schedule:
                    schedule_type = custom_schedule.get("type")
                    
                    if schedule_type == "content_based":
                        # Check for spikes before generating
                        spikes = await self.detect_spikes_for_newsletter(newsletter["id"])
                        if not spikes:
                            logger.info(f"No spikes detected for content-based newsletter {newsletter['id']}")
                            continue
                    
                    elif schedule_type == "trend_based":
                        # Check for trends before generating
                        trends = await self.detect_trends_for_newsletter(newsletter["id"])
                        if not trends:
                            logger.info(f"No trends detected for trend-based newsletter {newsletter['id']}")
                            continue
                
                # Generate the newsletter
                await self.generate_advanced_newsletter(newsletter["id"])
                
        except Exception as e:
            logger.error(f"Error processing advanced scheduled newsletters: {str(e)}")
    
    async def get_newsletter_insights(self, auto_newsletter_id: str) -> List[str]:
        """Get actionable insights for an auto-newsletter"""
        try:
            analytics = await self.get_newsletter_analytics(auto_newsletter_id)
            return analytics.get("insights", [])
        except Exception as e:
            logger.error(f"Error getting newsletter insights: {str(e)}")
            return []
